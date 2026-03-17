from __future__ import annotations

import logging
import uuid as _uuid
from contextlib import asynccontextmanager

import fastapi
from fastapi import staticfiles
from fastapi import templating
from fastapi.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware.trustedhost import TrustedHostMiddleware
from starlette.responses import Response

from backend.config import api_config
from backend.config import containers
from backend.config.paths import TEMPLATES_DIR, STATIC_DIR
from backend.src.infrastructure import github
from backend.src.infrastructure import blog

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app_: fastapi.FastAPI):
    cfg = api_config.get_config()
    app_.state.github_client = github.GitHubClient(
        username=cfg.github_username, token=cfg.github_token,
    )
    app_.state.blog_reader = blog.BlogReader(cfg.blog_dir)
    logger.info("Application started (debug=%s)", cfg.debug)
    yield
    logger.info("Application shut down")


class SecurityHeadersMiddleware:
    def __init__(self, app):  # type: ignore[no-untyped-def]
        self.app = app

    async def __call__(self, scope, receive, send):  # type: ignore[no-untyped-def]
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        cfg = api_config.get_config()

        async def send_with_headers(message):  # type: ignore[no-untyped-def]
            if message["type"] == "http.response.start":
                extra = [
                    (b"x-content-type-options", b"nosniff"),
                    (b"x-frame-options", b"DENY"),
                    (b"x-xss-protection", b"1; mode=block"),
                    (b"referrer-policy", b"strict-origin-when-cross-origin"),
                    (b"permissions-policy", b"camera=(), microphone=(), geolocation=()"),
                ]
                if not cfg.debug:
                    extra.append(
                        (b"strict-transport-security", b"max-age=63072000; includeSubDomains"),
                    )
                message["headers"] = list(message.get("headers", [])) + extra
            await send(message)

        await self.app(scope, receive, send_with_headers)


class RequestIdMiddleware:
    def __init__(self, app):  # type: ignore[no-untyped-def]
        self.app = app

    async def __call__(self, scope, receive, send):  # type: ignore[no-untyped-def]
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        request_id = str(_uuid.uuid4())
        for header_name, header_value in scope.get("headers", []):
            if header_name == b"x-request-id":
                request_id = header_value.decode()
                break
        scope.setdefault("state", {})["request_id"] = request_id

        async def send_with_request_id(message):  # type: ignore[no-untyped-def]
            if message["type"] == "http.response.start":
                message["headers"] = list(message.get("headers", [])) + [
                    (b"x-request-id", request_id.encode()),
                ]
            await send(message)

        await self.app(scope, receive, send_with_request_id)


def create_app() -> fastapi.FastAPI:
    cfg = api_config.get_config()

    logging.basicConfig(
        level=getattr(logging, cfg.log_level.upper(), logging.INFO),
        format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    app_ = fastapi.FastAPI(
        title=cfg.app_name,
        docs_url="/docs" if cfg.debug else None,
        redoc_url=None,
        lifespan=lifespan,
    )

    container = containers.ApplicationContainer()
    app_.container = container  # type: ignore[attr-defined]

    app_.add_middleware(
        CORSMiddleware,
        allow_origins=cfg.allowed_origins,
        allow_methods=["GET", "POST"],
        allow_headers=["*"],
    )

    if not cfg.debug and cfg.allowed_hosts:
        app_.add_middleware(TrustedHostMiddleware, allowed_hosts=cfg.allowed_hosts)

    app_.add_middleware(SecurityHeadersMiddleware)
    app_.add_middleware(RequestIdMiddleware)

    from backend.src.presentation.routers import projects, admin, index, blog as blog_router, pages
    app_.include_router(index.router)
    app_.include_router(projects.router)
    app_.include_router(blog_router.router)
    app_.include_router(pages.router)
    app_.include_router(admin.router)

    app_.mount("/static", staticfiles.StaticFiles(directory=STATIC_DIR), name="static")

    templates = templating.Jinja2Templates(directory=TEMPLATES_DIR)
    app_.state.templates = templates

    _register_error_handlers(app_, templates)

    return app_


def _register_error_handlers(
    app_: fastapi.FastAPI, templates: templating.Jinja2Templates,
) -> None:
    @app_.exception_handler(StarletteHTTPException)
    async def http_error(request: fastapi.Request, exc: StarletteHTTPException) -> Response:
        if exc.status_code == 401:
            return Response(
                status_code=401,
                headers=exc.headers or {"WWW-Authenticate": "Basic"},
            )
        if exc.status_code == 429:
            return templates.TemplateResponse(
                request, "errors/404.html", {"active_page": ""}, status_code=429,
            )
        tpl = "errors/404.html" if exc.status_code < 500 else "errors/500.html"
        return templates.TemplateResponse(
            request, tpl, {"active_page": ""}, status_code=exc.status_code,
        )

    @app_.exception_handler(Exception)
    async def unhandled_error(request: fastapi.Request, exc: Exception) -> Response:
        request_id = request.scope.get("state", {}).get("request_id", "unknown")
        logger.exception("Unhandled [request_id=%s]: %s %s", request_id, request.method, request.url)
        return templates.TemplateResponse(
            request, "errors/500.html", {"active_page": ""}, status_code=500,
        )


app = create_app()

from __future__ import annotations

import secrets
import time

import fastapi
from fastapi import security as security_

from backend.config import api_config

security = security_.HTTPBasic()

_MAX_ATTEMPTS = 5
_WINDOW_SEC = 300
_failed: dict[str, list[float]] = {}


def _check_rate_limit(client_ip: str) -> None:
    now = time.monotonic()
    attempts = _failed.get(client_ip, [])
    attempts = [t for t in attempts if now - t < _WINDOW_SEC]
    _failed[client_ip] = attempts
    if len(attempts) >= _MAX_ATTEMPTS:
        raise fastapi.HTTPException(
            status_code=429,
            detail="Too many login attempts. Try again later.",
        )


def _record_failure(client_ip: str) -> None:
    _failed.setdefault(client_ip, []).append(time.monotonic())


def _clear_failures(client_ip: str) -> None:
    _failed.pop(client_ip, None)


def require_admin(
    request: fastapi.Request,
    credentials: security_.HTTPBasicCredentials = fastapi.Depends(security),
) -> str:
    client_ip = request.client.host if request.client else "unknown"
    _check_rate_limit(client_ip)

    settings = api_config.get_config()
    username_ok = secrets.compare_digest(
        credentials.username.encode(), settings.admin_username.encode()
    )
    password_ok = secrets.compare_digest(
        credentials.password.encode(), settings.admin_password.encode()
    )
    if not (username_ok and password_ok):
        _record_failure(client_ip)
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    _clear_failures(client_ip)
    return credentials.username

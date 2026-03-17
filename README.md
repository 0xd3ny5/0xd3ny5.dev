<div align="center">

  <br />
  <br />

  <img src="https://img.shields.io/badge/FastAPI-backend-0F766E?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI" />
  <img src="https://img.shields.io/badge/PostgreSQL-database-334155?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL" />
  <img src="https://img.shields.io/badge/Docker-containerized-1D4ED8?style=for-the-badge&logo=docker&logoColor=white" alt="Docker" />
  <img src="https://img.shields.io/badge/Jinja2-templates-B91C1C?style=for-the-badge&logo=jinja&logoColor=white" alt="Jinja2" />

  <br />
  <br />

  <h1>denys.dev</h1>

  <p>
    Personal portfolio & blog with hex/8-bit aesthetic.
    <br />
  </p>

  <p>
    Portfolio · Blog · GitHub stats · Admin panel
  </p>

</div>

---

<h2>Overview</h2>

<h3>Features</h3>

<ul>
  <li>
    <strong>Portfolio with project management</strong><br />
    Admin-managed projects with draft/published states, featured flags, and tag-based categorisation.
  </li>
  <li>
    <strong>File-based blog</strong><br />
    Markdown posts with YAML frontmatter, cached rendering, and HTML sanitisation via <code>nh3</code>.
  </li>
  <li>
    <strong>Live GitHub stats</strong><br />
    Repos, stars, commits, followers — fetched from the GitHub API with built-in caching and retry logic.
  </li>
  <li>
    <strong>Admin panel</strong><br />
    HTTP Basic Auth with per-IP brute-force protection. CRUD for projects and blog posts.
  </li>
  <li>
    <strong>SEO out of the box</strong><br />
    Auto-generated <code>sitemap.xml</code>, <code>robots.txt</code>, Open Graph meta tags.
  </li>
  <li>
    <strong>Security headers</strong><br />
    HSTS, X-Frame-Options, X-Content-Type-Options, Referrer-Policy, Permissions-Policy, request IDs.
  </li>
  <li>
    <strong>Layered backend (DDD)</strong><br />
    Domain → Application → Infrastructure → Presentation, with IoC container and Unit of Work.
  </li>
</ul>

<br/>

<h2>Project Modules</h2>

<table>
  <tr>
    <td width="50%" valign="top">
      <h4>Portfolio (Projects)</h4>
      <blockquote>CRUD for portfolio projects with draft/publish workflow and featured flag.</blockquote>
      <table>
        <tr><td><strong>Domain</strong></td><td><code>Project</code> entity<br/><code>IProjectRepository</code>, <code>IProjectUnitOfWork</code></td></tr>
        <tr><td><strong>Application</strong></td><td><code>create</code>, <code>update</code>, <code>delete</code>, <code>get_published</code>, <code>get_all</code></td></tr>
        <tr><td><strong>Infrastructure</strong></td><td><code>ProjectModel</code> (SQLAlchemy), <code>PGProjectRepository</code>, <code>PGProjectUnitOfWork</code></td></tr>
        <tr><td><strong>Presentation</strong></td><td>Public routes (list / detail) + Admin routes (full CRUD + toggle publish)</td></tr>
      </table>
    </td>
    <td width="50%" valign="top">
      <h4>Blog</h4>
      <blockquote>File-based blog system — markdown posts with YAML frontmatter.</blockquote>
      <table>
        <tr><td><strong>Storage</strong></td><td>Markdown files in <code>blog_posts/</code></td></tr>
        <tr><td><strong>Parsing</strong></td><td><code>python-frontmatter</code> + <code>markdown</code> library</td></tr>
        <tr><td><strong>Sanitisation</strong></td><td><code>nh3</code> — whitelist of safe HTML tags and attributes</td></tr>
        <tr><td><strong>Caching</strong></td><td><code>lru_cache</code> keyed by file path + mtime</td></tr>
        <tr><td><strong>Admin</strong></td><td>Create / edit / delete posts via admin panel</td></tr>
      </table>
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <h4>GitHub Integration</h4>
      <blockquote>Live stats from GitHub API with caching and rate limit awareness.</blockquote>
      <table>
        <tr><td><strong>Stats</strong></td><td>Public repos, total stars, commits, followers</td></tr>
        <tr><td><strong>Client</strong></td><td><code>httpx</code> async client with retry logic</td></tr>
        <tr><td><strong>Cache TTL</strong></td><td>10 minutes (in-memory)</td></tr>
        <tr><td><strong>Frontend</strong></td><td>Animated counters via IntersectionObserver</td></tr>
      </table>
    </td>
    <td width="50%" valign="top">
      <h4>Admin Panel</h4>
      <blockquote>Protected CRUD interface for managing all site content.</blockquote>
      <table>
        <tr><td><strong>Auth</strong></td><td>HTTP Basic Auth with timing-safe comparison</td></tr>
        <tr><td><strong>Rate limiting</strong></td><td>5 attempts / 5 min per IP</td></tr>
        <tr><td><strong>Projects</strong></td><td>Create, edit, delete, toggle publish, set featured</td></tr>
        <tr><td><strong>Blog</strong></td><td>Create, edit, delete markdown posts</td></tr>
      </table>
    </td>
  </tr>
</table>

<br/>

<h2>API Endpoints</h2>

<h3>Public</h3>

| Method | Endpoint | Description |
|:--|:--|:--|
| `GET` | `/` | Portfolio home page |
| `GET` | `/projects/{id}` | Project detail page |
| `GET` | `/blog` | Blog listing |
| `GET` | `/blog/{slug}` | Blog post |
| `GET` | `/about` | About page |
| `GET` | `/api/projects` | Published projects (JSON) |
| `GET` | `/api/github-stats` | GitHub stats (JSON) |
| `GET` | `/health` | Health check |
| `GET` | `/robots.txt` | Robots for crawlers |
| `GET` | `/sitemap.xml` | Sitemap |

<h3>Admin (HTTP Basic Auth)</h3>

| Method | Endpoint | Description |
|:--|:--|:--|
| `GET` | `/admin` | Admin dashboard |
| `GET/POST` | `/admin/projects/new` | Create project |
| `GET/POST` | `/admin/projects/{id}/edit` | Edit project |
| `POST` | `/admin/projects/{id}/delete` | Delete project |
| `POST` | `/admin/projects/{id}/toggle-publish` | Toggle publish status |
| `GET/POST` | `/admin/blog/new` | Create blog post |
| `GET/POST` | `/admin/blog/{slug}/edit` | Edit blog post |
| `POST` | `/admin/blog/{slug}/delete` | Delete blog post |

<br/>

<h2>Quick Start</h2>

<blockquote>
Requirements: <strong>Docker</strong>, <strong>Docker Compose</strong>, <strong>Python 3.10+</strong>.
</blockquote>

<h3>1 — Clone & Configure</h3>

```bash
git clone <repo-url> && cd me

cp .env.example .env
# edit .env — set SECRET_KEY, ADMIN_PASSWORD, etc.
```

<h3>2 — Start Services</h3>

```bash
docker compose up -d --build
```

<table>
  <tr><th>Service</th><th>Port</th><th>Details</th></tr>
  <tr><td><strong>app</strong></td><td><code>8000</code></td><td>FastAPI via Uvicorn (2 workers)</td></tr>
  <tr><td><strong>db</strong></td><td>internal</td><td>PostgreSQL 16</td></tr>
</table>

Migrations run automatically on startup.

<h3>3 — Verify</h3>

```bash
curl http://localhost:8000/health
# → {"status": "ok"}
```

Open <code>http://localhost:8000</code> — portfolio.<br/>
Open <code>http://localhost:8000/admin</code> — admin panel.

<h3>Local Development (without Docker)</h3>

```bash
python -m pip install -e ".[dev]"
cp .env.example .env

createdb me
alembic upgrade head

uvicorn backend.main:app --reload --port 8000
```

<br/>

<h2>Configuration Reference</h2>

| Variable | Default | Description |
|:--|:--|:--|
| `APP_NAME` | `Denys - Backend Developer` | App display name |
| `DEBUG` | `false` | Debug mode (enables `/docs`) |
| `SECRET_KEY` | `change-me-in-production` | Random string, min 32 chars |
| `LOG_LEVEL` | `INFO` | Logging level |
| | | |
| `GITHUB_USERNAME` | `denyshub` | GitHub username for stats |
| `GITHUB_TOKEN` | — | GitHub PAT (optional, raises rate limit) |
| | | |
| `ADMIN_USERNAME` | `admin` | Admin panel login |
| `ADMIN_PASSWORD` | `admin` | Admin panel password |
| | | |
| `ALLOWED_ORIGINS` | `["http://localhost:8000"]` | CORS origins (JSON array) |
| `ALLOWED_HOSTS` | `[]` | Trusted host names (empty = disabled) |
| | | |
| `DATABASE_URL` | `postgresql+asyncpg://...` | PostgreSQL connection string |
| `DB_POOL_SIZE` | `5` | Connection pool size |
| `DB_MAX_OVERFLOW` | `10` | Max pool overflow |
| `DB_POOL_RECYCLE` | `300` | Connection recycle time (seconds) |

<br/>

<h2>Blog</h2>

Posts are markdown files in <code>blog_posts/</code> with YAML frontmatter:

```markdown
---
title: My First Post
date: 2026-03-10
tags: python, fastapi
description: A short description for the listing page.
cover: https://example.com/cover.jpg
---

## Content

Full **Markdown** support: code blocks, tables, lists, images.
```

Posts can be managed via the admin panel or by editing files directly.

<br/>

<h2>Security</h2>

<ul>
  <li><strong>HTTP Basic Auth</strong> — timing-safe credential comparison (<code>secrets.compare_digest</code>)</li>
  <li><strong>Brute-force protection</strong> — 5 failed attempts per IP → 429 for 5 minutes</li>
  <li><strong>Security headers</strong> — HSTS, X-Frame-Options (DENY), X-Content-Type-Options, Referrer-Policy, Permissions-Policy</li>
  <li><strong>Trusted hosts</strong> — optional <code>ALLOWED_HOSTS</code> to prevent host header attacks</li>
  <li><strong>HTML sanitisation</strong> — blog content sanitised via <code>nh3</code> with a strict tag whitelist</li>
  <li><strong>Path traversal protection</strong> — blog slugs validated against directory escape</li>
  <li><strong>CORS</strong> — configurable origin whitelist</li>
  <li><strong>Request IDs</strong> — unique ID per request for log correlation</li>
  <li><strong>Non-root container</strong> — Docker runs as <code>appuser</code></li>
  <li><strong>No exposed DB port</strong> — PostgreSQL is only accessible within the Docker network</li>
</ul>

<br/>

<h2>Production Checklist</h2>

Before deploying, make sure to:

- [ ] Set a strong `SECRET_KEY` (min 32 random chars)
- [ ] Change `ADMIN_PASSWORD` from the default
- [ ] Set `DEBUG=false`
- [ ] Configure `ALLOWED_ORIGINS` with your domain
- [ ] Configure `ALLOWED_HOSTS` with your domain
- [ ] Set production `DATABASE_URL`
- [ ] Place behind a reverse proxy (Nginx / Caddy) with TLS
- [ ] Set `GITHUB_TOKEN` for higher API rate limits

<br/>

<h2>Commands</h2>

| Command | Description |
|:--|:--|
| `uvicorn backend.main:app --reload` | Dev server with hot reload |
| `alembic upgrade head` | Apply all pending migrations |
| `alembic revision --autogenerate -m "msg"` | Generate new migration |
| `pytest -v` | Run tests |
| `mypy backend/` | Type check |
| `ruff check .` | Lint |
| `docker compose up -d --build` | Start all services |

<br/>

---

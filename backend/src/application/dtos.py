from __future__ import annotations

import uuid

import pydantic


class ProjectCreateDTO(pydantic.BaseModel):
    title: str
    short_description: str = ""
    full_description: str = ""
    tags: list[str] = []
    github_url: str = ""
    live_url: str = ""
    cover_image: str = ""
    is_featured: bool = False
    is_published: bool = False
    sort_order: int = 0


class ProjectUpdateDTO(pydantic.BaseModel):
    id: uuid.UUID
    title: str | None = None
    short_description: str | None = None
    full_description: str | None = None
    tags: list[str] | None = None
    github_url: str | None = None
    live_url: str | None = None
    cover_image: str | None = None
    is_featured: bool | None = None
    is_published: bool | None = None
    sort_order: int | None = None

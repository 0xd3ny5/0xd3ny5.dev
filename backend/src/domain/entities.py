from __future__ import annotations

import datetime
import uuid

import pydantic


class Project(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(from_attributes=True)

    id: uuid.UUID = pydantic.Field(default_factory=uuid.uuid4)
    sort_order: int = 0
    title: str = ""
    short_description: str = ""
    full_description: str = ""
    tags: list[str] = []
    github_url: str = ""
    live_url: str = ""
    cover_image: str = ""
    is_featured: bool = False
    is_published: bool = False
    created_at: datetime.datetime | None = None

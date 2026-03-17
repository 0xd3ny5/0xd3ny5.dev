import typing

from backend.src.domain import entities
from backend.src.infrastructure import models


class ProjectMapper:
    __slots__: typing.Sequence[str] = ()

    def to_entity(self, model: models.ProjectModel) -> entities.Project:
        return entities.Project(
            id=model.id,
            title=model.title,
            short_description=model.short_description,
            full_description=model.full_description,
            tags=[t.strip() for t in model.tags.split(",") if t.strip()] if model.tags else [],
            github_url=model.github_url,
            live_url=model.live_url,
            cover_image=model.cover_image,
            is_featured=model.is_featured,
            is_published=model.is_published,
            sort_order=model.sort_order,
            created_at=model.created_at,
        )

    def to_model(self, entity: entities.Project) -> models.ProjectModel:
        return models.ProjectModel(
            id=entity.id,
            title=entity.title,
            short_description=entity.short_description,
            full_description=entity.full_description,
            tags=",".join(entity.tags),
            github_url=entity.github_url,
            live_url=entity.live_url,
            cover_image=entity.cover_image,
            is_featured=entity.is_featured,
            is_published=entity.is_published,
            sort_order=entity.sort_order,
        )

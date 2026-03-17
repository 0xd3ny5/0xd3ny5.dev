from __future__ import annotations

import typing

from dependency_injector import containers
from dependency_injector import providers

from backend.src.infrastructure import orm
from backend.src.infrastructure import uow as uow_impl
from backend.config import api_config

if typing.TYPE_CHECKING:
    from backend.src.domain import uow


class ApplicationContainer(containers.DeclarativeContainer):
    # FIXME: Hardcode ?
    wiring_config = containers.WiringConfiguration(
        modules=[
            "backend.src.presentation.routers.projects",
            "backend.src.presentation.routers.admin",
            "backend.src.presentation.routers.index",
        ],
    )

    config = providers.Configuration()
    config.from_dict(api_config.get_config().model_dump())

    engine = providers.Singleton(orm.create_async_engine, config.database_url, config.echo)
    sessionmaker = providers.Singleton(orm.create_async_session, engine)

    project_uow: uow.IProjectUnitOfWork = providers.Factory(
        uow_impl.PGProjectUnitOfWork,
        session_factory=sessionmaker,
    )

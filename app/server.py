from __future__ import annotations

from fastapi import FastAPI

from app.core.logging import configure_logging
from app.modules.coord_to_geohash.api.router import router as coord_to_geohash_router
from app.modules.home.api.router import router as home_router


def create_app() -> FastAPI:
    configure_logging()

    application = FastAPI(
        title="Boolish Helper",
        description="Ferramentas ad hoc modulares para tarefas do dia a dia.",
        version="2.0.0",
    )

    application.include_router(home_router)
    application.include_router(coord_to_geohash_router)

    return application


app = create_app()

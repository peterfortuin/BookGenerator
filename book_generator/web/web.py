from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from containers.book_generator_container import book_generator_container
from . import websocket, index


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)
    app.container = book_generator_container
    app.mount("/renders", StaticFiles(directory="renders"), name="static")
    app.mount("/static", StaticFiles(directory="static"), name="static")
    app.include_router(websocket.router)
    app.include_router(index.router)
    return app


fast_api = create_app()

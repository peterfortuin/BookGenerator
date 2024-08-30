from contextlib import asynccontextmanager

from dependency_injector.wiring import Provide, inject
from fastapi import FastAPI, Depends
from starlette.staticfiles import StaticFiles

from containers.book_generator_container import book_generator_container, BookGeneratorContainer
from services.book_service import BookService
from . import websocket, index
from .websocket import start_queue_listener


@asynccontextmanager
@inject
async def lifespan(app: FastAPI, book_service: BookService = Depends(Provide[BookGeneratorContainer.book_service])):
    await start_queue_listener(book_service.event_queue)
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

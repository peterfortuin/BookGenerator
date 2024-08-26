import os
from typing import Optional

from dependency_injector.wiring import inject, Provide
from fastapi import FastAPI, Depends
from fastapi.responses import HTMLResponse
from starlette.requests import Request
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from containers.book_generator_container import BookGeneratorContainer, book_generator_container
from services.book_service import BookService


def create_app() -> FastAPI:
    app = FastAPI()
    app.container = book_generator_container
    app.mount("/renders", StaticFiles(directory="renders"), name="static")
    app.mount("/static", StaticFiles(directory="static"), name="static")
    return app


fast_api = create_app()
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates'))


@fast_api.get("/", response_class=HTMLResponse)
@inject
async def read_book(request: Request,
                    book_service: BookService = Depends(Provide[BookGeneratorContainer.book_service])):
    render_dir = book_service.get_render_dir()
    number_of_pages = book_service.get_number_of_pages()
    return templates.TemplateResponse(request, "book.html", {"render_dir": render_dir, "number_of_pages": number_of_pages})

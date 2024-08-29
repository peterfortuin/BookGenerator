import os

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter
from fastapi.params import Depends
from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates

from containers.book_generator_container import BookGeneratorContainer
from services.book_service import BookService

router = APIRouter()
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates'))


@router.get("/", response_class=HTMLResponse)
@inject
async def read_book(
        request: Request,
        book_service: BookService = Depends(Provide[BookGeneratorContainer.book_service])
):
    render_dir = book_service.get_render_dir()
    number_of_pages = book_service.get_number_of_pages()
    return templates.TemplateResponse(
        request,
        "book.html",
        {"render_dir": render_dir, "number_of_pages": number_of_pages}
    )

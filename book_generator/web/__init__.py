import os

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from starlette.requests import Request
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

fast_api = FastAPI()
fast_api.mount("/renders", StaticFiles(directory="renders"), name="static")
fast_api.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates'))


@fast_api.get("/", response_class=HTMLResponse)
async def read_book(request: Request):
    return templates.TemplateResponse(request, "book.html", {})

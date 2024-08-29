import asyncio
from enum import Enum

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter
from fastapi.params import Depends
from pydantic import BaseModel
from starlette.websockets import WebSocket

from containers.book_generator_container import BookGeneratorContainer
from services.book_service import BookService


class WebSocketMessageTypes(Enum):
    BookRenderingStart = "BookRenderingStart"
    BookRenderingComplete = "BookRenderingComplete"
    BookScriptException = "BookScriptException"


class WebSocketMessage(BaseModel):
    type: WebSocketMessageTypes
    data: str | None = None


router = APIRouter()


@router.websocket("/ws")
@inject
async def websocket_endpoint(
        websocket: WebSocket,
        book_service: BookService = Depends(Provide[BookGeneratorContainer.book_service])
):
    await websocket.accept()

    await websocket.send_json(
        WebSocketMessage(type=WebSocketMessageTypes.BookRenderingComplete,
                         data=str(book_service.get_number_of_pages())).model_dump_json())

    while True:
        event = await book_service.wait_until_event()

        if event["state"] == "rendering":
            await websocket.send_json(
                WebSocketMessage(type=WebSocketMessageTypes.BookRenderingStart, data=None).model_dump_json())
        elif event["state"] == "rendering_completed":
            await websocket.send_json(
                WebSocketMessage(type=WebSocketMessageTypes.BookRenderingComplete,
                                 data=str(book_service.get_number_of_pages())).model_dump_json())
        else:
            raise Exception(f"Unknown state: {event['state']}")

import asyncio
from enum import Enum
from queue import Queue

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter
from fastapi.params import Depends
from pydantic import BaseModel
from starlette.websockets import WebSocket, WebSocketDisconnect

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
connected_clients: list[WebSocket] = list()


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

    connected_clients.append(websocket)
    try:
        while True:
            received_message = await websocket.receive_text()
            print(f"Received message: {received_message}")
    except WebSocketDisconnect:
        connected_clients.remove(websocket)
        print("WebSocket disconnected")


background_tasks = set()


async def start_queue_listener(queue: Queue):
    task = asyncio.create_task(process_queue(queue))
    background_tasks.add(task)
    task.add_done_callback(background_tasks.discard)


async def process_queue(event_queue: Queue):
    while True:
        event = await event_queue.get()

        if event["state"] == "rendering":
            await broadcast_message(WebSocketMessage(type=WebSocketMessageTypes.BookRenderingStart, data=None))
        elif event["state"] == "rendering_completed":
            await broadcast_message(WebSocketMessage(type=WebSocketMessageTypes.BookRenderingComplete, data=None))
        else:
            raise Exception(f"Unknown state: {event['state']}")


async def broadcast_message(json: WebSocketMessage):
    for client in connected_clients:
        try:
            # await client.send_json(json)
            await client.send_json(json.model_dump_json())
        except WebSocketDisconnect:
            connected_clients.remove(client)


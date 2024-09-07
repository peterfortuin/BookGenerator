import asyncio
from enum import Enum
from queue import Queue
from typing import Optional, List

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter
from fastapi.params import Depends
from pydantic import BaseModel
from starlette.websockets import WebSocket, WebSocketDisconnect

from containers.book_generator_container import BookGeneratorContainer
from generator.book import RenderUpdate, RenderState
from services.book_service import BookService


class WebSocketMessageTypes(Enum):
    BookRenderingStart = "BookRenderingStart"
    BookRenderingComplete = "BookRenderingComplete"
    BookScriptException = "BookScriptException"


class WebSocketMessage(BaseModel):
    type: WebSocketMessageTypes
    data: Optional[List[str]] = None


router = APIRouter()
connected_clients: list[WebSocket] = list()

last_update: Optional[WebSocketMessage] = None


@router.websocket("/ws")
@inject
async def websocket_endpoint(
        websocket: WebSocket,
        book_service: BookService = Depends(Provide[BookGeneratorContainer.book_service])
):
    await websocket.accept()

    if last_update is not None:
        json = last_update.model_dump_json()
    else:
        json = WebSocketMessage(type=WebSocketMessageTypes.BookRenderingStart, data=[]).model_dump_json()

    await websocket.send_json(json)

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
    global last_update

    while True:
        update: RenderUpdate = await event_queue.get()
        print(f"Received update: {update}")

        if update.state == RenderState.RENDERING:
            last_update = WebSocketMessage(type=WebSocketMessageTypes.BookRenderingStart, data=update.page_paths)
            await broadcast_message(
                last_update
            )
        elif update.state == RenderState.COMPLETED:
            last_update = WebSocketMessage(type=WebSocketMessageTypes.BookRenderingComplete, data=update.page_paths)
            await broadcast_message(
                last_update
            )
        else:
            raise Exception(f"Unknown state: {update.state}")


async def broadcast_message(json: WebSocketMessage):
    for client in connected_clients:
        try:
            await client.send_json(json.model_dump_json())
        except WebSocketDisconnect:
            connected_clients.remove(client)

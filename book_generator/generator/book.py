import asyncio
import os
from asyncio import Queue
from enum import Enum, auto, IntEnum
from typing import Dict, List

from generator.spread import Spread


class RenderState(IntEnum):
    RENDERING = auto()
    COMPLETED = auto()


class RenderUpdate:
    def __init__(self, state: RenderState, page_paths: List[str]):
        self.state = state
        self.page_paths = page_paths

    def __str__(self):
        return f"RenderUpdate(state={self.state}, number_of_pages={len(self.page_paths)})"


class Book:
    def __init__(self, name: str, width_in_cm: float, height_in_cm: float, *spreads: Spread):
        self.spreads = list(spreads)
        self.name = name
        self.render_dir = f"renders/{self.name}"
        self.width_in_cm = width_in_cm
        self.height_in_cm = height_in_cm
        self._render_events = asyncio.Event()
        self._render_result = None
        self.page_paths = []

    async def render_all_spreads(self, event_queue: Queue):
        os.makedirs(self.render_dir, exist_ok=True)

        for index, spread in enumerate(self.spreads):
            await event_queue.put(RenderUpdate(RenderState.RENDERING, self.page_paths))

            page_number = index * 2 + 1
            print(f"Rendering spread {index + 1} of {len(self.spreads)}.")
            (file_path_l, file_path_r) = spread.render(self, self.render_dir, page_number)

            if 0 <= index * 2 < len(self.page_paths):
                self.page_paths[index] = file_path_l
                self.page_paths[index + 1] = file_path_r
            else:
                self.page_paths.append(file_path_l)
                self.page_paths.append(file_path_r)

        await event_queue.put(RenderUpdate(RenderState.COMPLETED, self.page_paths))

    def fire_event(self, data: Dict[str, str]):
        print(f"Book event: {data["state"]}")
        self._render_result = data
        self._render_events.set()

    async def wait_until_event(self) -> Dict[str, str]:
        await self._render_events.wait()
        self._render_events.clear()
        return self._render_result

    def get_page_size(self) -> (int, int):
        return int(self.width_in_cm / 2.54 * 300), int(self.height_in_cm / 2.54 * 300)

    def get_number_of_pages(self) -> int:
        return len(self.spreads) * 2

    def get_render_dir(self) -> str:
        return self.render_dir

import asyncio
import os
from typing import Dict

from generator.spread import Spread


class Book:
    def __init__(self, name: str, width_in_cm: float, height_in_cm: float, *spreads: Spread):
        self.spreads = list(spreads)
        self.name = name
        self.render_dir = f"renders/{self.name}"
        self.width_in_cm = width_in_cm
        self.height_in_cm = height_in_cm
        self._render_events = asyncio.Event()
        self._render_result = None

    async def render_all_spreads(self):
        self.fire_event({"state": "rendering"})

        os.makedirs(self.render_dir, exist_ok=True)

        for index, spread in enumerate(self.spreads):
            page_number = index * 2 + 1
            print(f"Rendering spread {index + 1} of {len(self.spreads)}.")
            spread.render(self, self.render_dir, page_number)

        self.fire_event({"state": "rendering_completed"})

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

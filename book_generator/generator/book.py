import os

from generator.spread import Spread


class Book:
    def __init__(self, name: str, width_in_cm: float, height_in_cm: float, *spreads: Spread):
        self.spreads = list(spreads)
        self.name = name
        self.render_dir = f"renders/{self.name}"
        self.width_in_cm = width_in_cm
        self.height_in_cm = height_in_cm

    def render_all_spreads(self) -> int:
        os.makedirs(self.render_dir, exist_ok=True)

        for index, spread in enumerate(self.spreads):
            page_number = index * 2 + 1
            print(f"Rendering spread {index + 1} of {len(self.spreads)}.")
            spread.render(self, self.render_dir, page_number)

    def get_page_size(self) -> (int, int):
        return int(self.width_in_cm / 2.54 * 300), int(self.height_in_cm / 2.54 * 300)

    def get_number_of_pages(self) -> int:
        return len(self.spreads) * 2

    def get_render_dir(self) -> str:
        return self.render_dir

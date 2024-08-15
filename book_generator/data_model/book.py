import os

from data_model.page import Page
from data_model.spread import Spread
from PIL import Image


class Book:
    def __init__(self, name: str, width_in_cm: float, height_in_cm: float, *spreads: Spread):
        self.spreads = list(spreads)
        self.name = name
        self.render_dir = f"renders/{self.name}"
        self.width_in_cm = width_in_cm
        self.height_in_cm = height_in_cm

    def render_all_spreads(self):
        os.makedirs(self.render_dir, exist_ok=True)

        for index, spread in enumerate(self.spreads):
            page_number = index * 2 + 1
            spread.render(self, self.render_dir, page_number)

    def get_page_size(self) -> (int, int):
        return int(self.width_in_cm / 2.54 * 300), int(self.height_in_cm / 2.54 * 300)

    def create_empty_page(self, render_path: str) -> Page:
        return Page(
            Image.new("RGB", self.get_page_size(), color=0xFFFFFF),
            render_path,
        )

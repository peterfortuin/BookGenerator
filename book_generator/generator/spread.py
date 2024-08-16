import logging
from abc import abstractmethod

from PIL import Image

from generator.template import TwoPageTemplate, OnePageTemplate

logger = logging.getLogger("spread")


class Spread:
    @abstractmethod
    def render(self, book: 'Book', render_dir: str, page_number: int):
        pass

    @staticmethod
    def get_render_section(width_in_cm: float, height_in_cm: float):
        width_in_pixels = int(width_in_cm / 2.54 * 300)
        height_in_pixels = int(height_in_cm / 2.54 * 300)
        return Image.new("RGB", (width_in_pixels, height_in_pixels), color=0xFFFFFF)

    @staticmethod
    def save(image: Image, render_dir: str, page_number: int):
        render_path = f"{render_dir}/page_{page_number:03d}.jpg"
        image.save(render_path)


class TwoPageTemplateSpread(Spread):
    def __init__(self, template: TwoPageTemplate):
        self.template = template

    def render(self, book: 'Book', render_dir: str, page_number: int):
        logger.info(f"Rendering page {page_number}")
        self.template.render(self.get_render_section(book.width_in_cm * 2, book.height_in_cm))
        self.save(render_dir, page_number)


class TwoSinglePagesTemplateSpread(Spread):
    def __init__(self, left_template: OnePageTemplate, right_template: OnePageTemplate):
        self.left_template = left_template
        self.right_template = right_template

    def render(self, book: 'Book', render_dir: str, page_number: int):
        logger.info(f"Rendering page {page_number}")
        left_image = self.left_template.render(self.get_render_section(book.width_in_cm, book.height_in_cm))
        self.save(left_image, render_dir, page_number)

        logger.info(f"Rendering page {page_number + 1}")
        right_image = self.right_template.render(self.get_render_section(book.width_in_cm, book.height_in_cm))
        self.save(right_image, render_dir, page_number + 1)

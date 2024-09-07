import logging
from abc import abstractmethod

from PIL import Image

from generator.template import TwoPageTemplate, OnePageTemplate

logger = logging.getLogger("spread")


class Spread:
    @abstractmethod
    def render(self, book: 'Book', render_dir: str, page_number: int) -> (str, str):
        pass

    @staticmethod
    def get_render_section(width_in_cm: float, height_in_cm: float):
        width_in_pixels = int(width_in_cm / 2.54 * 300)
        height_in_pixels = int(height_in_cm / 2.54 * 300)

        return Image.new("RGBA", (width_in_pixels, height_in_pixels), color=0xFFFFFF)

    def save(self, image: Image, render_dir: str, suffix: str) -> str:
        positive_hash = abs(hash(self))

        image = image.convert("RGB")

        file_path = f"{render_dir}/page_{positive_hash}_{suffix}.jpeg"
        image.save(file_path, dpi=(300, 300), quality=100)

        return file_path

    def __eq__(self, other):
        if isinstance(other, Spread):
            return vars(self) == vars(other)
        return False

    def __hash__(self):
        return hash(tuple(sorted(vars(self).items())))


class TwoPageTemplateSpread(Spread):
    def __init__(self, template: TwoPageTemplate):
        self.template = template

    def render(self, book: 'Book', render_dir: str, page_number: int) -> (str, str):
        logger.info(f"Rendering page {page_number}")
        spread_image = self.template.render(self.get_render_section(book.width_in_cm * 2, book.height_in_cm))
        left_page = spread_image.crop((0, 0, spread_image.width / 2, spread_image.height))
        right_page = spread_image.crop((spread_image.width / 2, 0, spread_image.width, spread_image.height))
        file_path_l = self.save(left_page, render_dir, "l")
        file_path_r = self.save(right_page, render_dir, "r")

        return file_path_l, file_path_r


class TwoSinglePagesTemplateSpread(Spread):
    def __init__(self, left_template: OnePageTemplate, right_template: OnePageTemplate):
        self.left_template = left_template
        self.right_template = right_template

    def render(self, book: 'Book', render_dir: str, page_number: int) -> (str, str):
        logger.info(f"Rendering page {page_number}")
        left_image = self.left_template.render(self.get_render_section(book.width_in_cm, book.height_in_cm))
        file_path_l = self.save(left_image, render_dir, "l")

        logger.info(f"Rendering page {page_number + 1}")
        right_image = self.right_template.render(self.get_render_section(book.width_in_cm, book.height_in_cm))
        file_path_r = self.save(right_image, render_dir, "r")

        return file_path_l, file_path_r
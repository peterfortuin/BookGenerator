import logging
from abc import abstractmethod

from data_model.template import TwoPageTemplate, OnePageTemplate

logger = logging.getLogger("spread")


class Spread:
    @abstractmethod
    def render(self, book: 'Book', render_dir: str, page_number: int):
        pass


class TwoPageTemplateSpread(Spread):
    def __init__(self, template: TwoPageTemplate):
        self.template = template

    def render(self, book: 'Book', render_dir: str, page_number: int):
        logger.info(f"Rendering page {page_number}")
        self.template.render(book, f"{render_dir}/page_f{page_number: 04d}.jpg")


class TwoSinglePagesTemplateSpread(Spread):
    def __init__(self, left_template: OnePageTemplate, right_template: OnePageTemplate):
        self.left_template = left_template
        self.right_template = right_template

    def render(self, book: 'Book', render_dir: str, page_number: int):
        logger.info(f"Rendering page {page_number}")
        self.left_template.render(book, f"{render_dir}/page_{page_number:03d}.jpg")
        logger.info(f"Rendering page {page_number + 1}")
        self.right_template.render(book, f"{render_dir}/page_{(page_number + 1):03d}.jpg")

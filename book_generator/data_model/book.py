import os

from book_generator.data_model.page import Page


class Book:
    def __init__(self, name: str, *pages: Page):
        self.pages = pages
        self.name = name
        self.render_dir = f"renders/{self.name}"

    def add_page(self, page):
        self.pages.append(page)

    def render_all_pages(self):
        os.makedirs(self.render_dir, exist_ok=True)

        for page in self.pages:
            page.render(self)

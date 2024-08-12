from book_generator.data_model.page import Page


class Book:
    def __init__(self, *pages: Page):
        self.pages = pages

    def add_page(self, page):
        self.pages.append(page)

    def render(self):
        for page in self.pages:
            page.render()

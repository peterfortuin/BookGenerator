from data_model.book import Book
from data_model.photo import Photo
from data_model.template import OnePageTemplate


class OnePhotoTemplate(OnePageTemplate):
    def __init__(self, photo: Photo):
        self.photo = photo

    def render(self, book: Book, render_path: str):
        page = book.create_empty_page(render_path)
        page.draw_image(self.photo, 0, 0, 100, 100)
        page.save()

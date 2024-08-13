from data_model.book import Book


class Page:
    def __init__(self, *elements) -> None:
        self.elements = list(elements)

    def add_element(self, element):
        self.elements.append(element)

    def render(self, book: Book):
        for element in self.elements:
            element.render()

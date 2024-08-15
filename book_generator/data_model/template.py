from abc import abstractmethod


class Template:

    @abstractmethod
    def render(self, book: 'Book', render_path: str):
        pass


class OnePageTemplate(Template):
    @abstractmethod
    def render(self, book: 'Book', render_path: str):
        pass


class TwoPageTemplate(Template):
    @abstractmethod
    def render(self, book: 'Book', render_path: str):
        pass

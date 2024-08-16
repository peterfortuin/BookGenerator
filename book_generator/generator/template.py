from abc import abstractmethod

from PIL.Image import Image


class Template:

    @abstractmethod
    def render(self, image: Image) -> Image:
        pass


class OnePageTemplate(Template):
    @abstractmethod
    def render(self, image: Image) -> Image:
        pass


class TwoPageTemplate(Template):
    @abstractmethod
    def render(self, image: Image) -> Image:
        pass

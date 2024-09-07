from abc import abstractmethod

from PIL.Image import Image


class Template:

    @abstractmethod
    def render(self, image: Image) -> Image:
        pass

    def __eq__(self, other):
        if isinstance(other, Template):
            return vars(self) == vars(other)
        return False

    def __hash__(self):
        return hash(tuple(sorted(vars(self).items())))


class OnePageTemplate(Template):
    @abstractmethod
    def render(self, image: Image) -> Image:
        pass


class TwoPageTemplate(Template):
    @abstractmethod
    def render(self, image: Image) -> Image:
        pass

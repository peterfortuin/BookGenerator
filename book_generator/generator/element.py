from abc import abstractmethod

from PIL import Image


class Element:

    def __eq__(self, other):
        if isinstance(other, Element):
            return vars(self) == vars(other)
        return False

    def __hash__(self):
        return hash(tuple(sorted(vars(self).items())))

    @abstractmethod
    def render(self, image: Image) -> Image:
        pass

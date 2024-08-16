from abc import abstractmethod

from PIL import Image


class Element:
    @abstractmethod
    def render(self, image: Image) -> Image:
        pass

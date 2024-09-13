from PIL.Image import Image

from generator.template import OnePageTemplate


class EmptyTemplate(OnePageTemplate):

    def render(self, image: Image) -> Image:
        return image

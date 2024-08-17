from PIL.Image import Image

from generator.photo import Photo
from generator.template import OnePageTemplate
from generator.utils import draw_on_region


class OnePhotoTemplate(OnePageTemplate):
    def __init__(self, photo: Photo):
        self.photo = photo

    def render(self, image: Image) -> Image:
        return draw_on_region(image, 0, 0, 100, 100, self.photo.render)

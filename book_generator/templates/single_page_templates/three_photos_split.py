from PIL.Image import Image

from generator.photo import Photo
from generator.template import OnePageTemplate
from generator.utils import draw_on_region


class ThreePhotosSplitTemplate(OnePageTemplate):
    def __init__(self,
                 big_photo: Photo,
                 small_photo1: Photo,
                 small_photo2: Photo,
                 outside_margins: float = 0,
                 inside_margins: float = 0,
                 horizontal_split: float = 50,
                 vertical_split: float = 50,
                 ):
        self.big_photo = big_photo
        self.small_photo1 = small_photo1
        self.small_photo2 = small_photo2
        self.outside_margins = outside_margins
        self.inside_margins = inside_margins
        self.horizontal_split = horizontal_split
        self.vertical_split = vertical_split

    def render(self, image: Image) -> Image:
        image = draw_on_region(
            image,
            self.outside_margins,
            self.outside_margins,
            self.vertical_split - self.inside_margins / 2,
            self.horizontal_split - self.inside_margins / 2,
            self.small_photo1.render
        )
        image = draw_on_region(
            image,
            self.vertical_split + self.inside_margins / 2,
            self.outside_margins,
            100 - self.outside_margins,
            self.horizontal_split - self.inside_margins / 2,
            self.small_photo2.render
        )
        image = draw_on_region(
            image,
            self.outside_margins,
            self.horizontal_split + self.inside_margins / 2,
            100 - self.outside_margins,
            100 - self.outside_margins,
            self.big_photo.render
        )

        return image

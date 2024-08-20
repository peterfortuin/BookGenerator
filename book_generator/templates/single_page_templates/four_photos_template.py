from PIL.Image import Image

from generator.photo import Photo
from generator.template import OnePageTemplate
from generator.utils import draw_on_region


class FourPhotosTemplate(OnePageTemplate):
    def __init__(self,
                 photo1: Photo,
                 photo2: Photo,
                 photo3: Photo,
                 photo4: Photo,
                 outside_margins: float = 0,
                 inside_margins: float = 0,
                 horizontal_split: float = 50,
                 vertical_split: float = 50,
                 ):
        self.photo1 = photo1
        self.photo2 = photo2
        self.photo3 = photo3
        self.photo4 = photo4
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
            self.photo1.render
        )
        image = draw_on_region(
            image,
            self.vertical_split + self.inside_margins / 2,
            self.outside_margins,
            100 - self.outside_margins,
            self.horizontal_split - self.inside_margins / 2,
            self.photo2.render
        )
        image = draw_on_region(
            image,
            self.outside_margins,
            self.horizontal_split + self.inside_margins / 2,
            self.vertical_split - self.inside_margins / 2,
            100 - self.outside_margins,
            self.photo3.render
        )
        image = draw_on_region(
            image,
            self.vertical_split + self.inside_margins / 2,
            self.horizontal_split + self.inside_margins / 2,
            100 - self.outside_margins,
            100 - self.outside_margins,
            self.photo4.render
        )

        return image

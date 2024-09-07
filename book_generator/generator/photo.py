from urllib.request import urlopen

from PIL import Image, ImageOps

from generator.element import Element
from generator.utils import transparent_color, correct_image_orientation


class Photo(Element):

    def __init__(self, path, render_inside: bool = False, centering: int = 50):
        self.path = path
        self.render_inside = render_inside
        self.centering = centering

        if self.path.startswith(("http://", "https://")):
            self.photo = Image.open(urlopen(self.path))
        else:
            self.photo = Image.open(path)

        self.photo = correct_image_orientation(self.photo)

    def __eq__(self, other):
        if isinstance(other, Photo):
            return (self.path, self.render_inside, self.centering) == (other.path, other.render_inside, other.centering)
        return False

    def __hash__(self):
        return hash((self.path, self.render_inside, self.centering))

    def render(self, image: Image) -> Image:
        render_size = (image.width, image.height)
        photo_rgba = self.photo.convert('RGBA')

        if self.render_inside:
            resized_image = ImageOps.pad(
                photo_rgba,
                render_size,
                color=transparent_color,
                centering=(self.centering / 100.0, self.centering / 100.0)
            )
        else:
            resized_image = ImageOps.fit(
                photo_rgba,
                render_size,
                centering=(self.centering / 100.0, self.centering / 100.0)
            )

        return resized_image

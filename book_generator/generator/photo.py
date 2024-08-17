from urllib.request import urlopen

from PIL import ImageDraw, Image
from PIL.Image import Resampling

from generator.element import Element


class Photo(Element):

    def __init__(self, path):
        self.path = path

        if self.path.startswith(("http://", "https://")):
            self.photo = Image.open(urlopen(self.path))
        else:
            self.photo = Image.open(path)

    def render(self, image: Image) -> Image:
        # Debug rectangles
        # draw = ImageDraw.Draw(image)
        # draw.rectangle((0, 0, image.width - 1, image.height - 1), fill=None, outline=0)

        # Calculate the scaling factor to maintain aspect ratio
        src_width, src_height = self.photo.size
        scale_factor = min(image.width / src_width, image.height / src_height)

        # Calculate the new size of the src_img while maintaining aspect ratio
        new_width = int(src_width * scale_factor)
        new_height = int(src_height * scale_factor)

        # Resize the source image
        resized_src_img = self.photo.resize((new_width, new_height), Resampling.LANCZOS)

        # Calculate position to center the resized image in the target box
        paste_x = (image.width - new_width) // 2
        paste_y = (image.height - new_height) // 2

        # Paste the resized image onto the destination image
        image.paste(resized_src_img, (paste_x, paste_y))

        return image

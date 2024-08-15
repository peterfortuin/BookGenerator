from PIL import Image, ImageDraw
from PIL.Image import Resampling

from data_model.photo import Photo


class Page:
    def __init__(self, image: Image, render_path: str):
        self.image = image
        self.render_path = render_path

    def draw_image(self, photo: Photo, x1: int, y1: int, x2: int, y2: int):
        # Ensure x1, y1, x2, y2 are within the range [0, 100]
        x1 = max(0, min(100, x1))
        y1 = max(0, min(100, y1))
        x2 = max(0, min(100, x2))
        y2 = max(0, min(100, y2))

        # Convert percentages to pixel values
        dst_width, dst_height = self.image.size
        left = int(x1 / 100 * dst_width)
        top = int(y1 / 100 * dst_height)
        right = int(x2 / 100 * dst_width)
        bottom = int(y2 / 100 * dst_height)

        draw = ImageDraw.Draw(self.image)
        draw.rectangle((left, top, right, bottom), fill=None, outline=0)

        # Calculate the target box dimensions
        target_width = right - left
        target_height = bottom - top

        # Calculate the scaling factor to maintain aspect ratio
        src_width, src_height = photo.image.size
        scale_factor = min(target_width / src_width, target_height / src_height)

        # Calculate the new size of the src_img while maintaining aspect ratio
        new_width = int(src_width * scale_factor)
        new_height = int(src_height * scale_factor)

        # Resize the source image
        resized_src_img = photo.image.resize((new_width, new_height), Resampling.LANCZOS)

        # Calculate position to center the resized image in the target box
        paste_x = left + (target_width - new_width) // 2
        paste_y = top + (target_height - new_height) // 2

        # Paste the resized image onto the destination image
        self.image.paste(resized_src_img, (paste_x, paste_y))

    def save(self):
        self.image.save(self.render_path)

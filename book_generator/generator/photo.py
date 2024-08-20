from urllib.request import urlopen

from PIL import Image, ExifTags
from PIL.Image import Resampling, Transpose

from generator.element import Element


class Photo(Element):

    def __init__(self, path, render_inside: bool = False, crop_bias: int = 50):
        self.path = path
        self.render_inside = render_inside
        self.crop_bias = crop_bias

        if self.path.startswith(("http://", "https://")):
            self.photo = Image.open(urlopen(self.path))
        else:
            self.photo = Image.open(path)

        self.photo = correct_image_orientation(self.photo)

    def render(self, image: Image) -> Image:
        # Ensure crop_bias is between 0 and 100
        crop_bias = max(0, min(100, self.crop_bias))

        # Calculate the scaling factor to maintain aspect ratio
        src_width, src_height = self.photo.size

        if self.render_inside:
            # Scale to fit inside the target image
            scale_factor = min(image.width / src_width, image.height / src_height)
        else:
            # Scale to fill the target image and crop excess
            scale_factor = max(image.width / src_width, image.height / src_height)

        # Calculate the new size of the src_img while maintaining aspect ratio
        new_width = int(src_width * scale_factor)
        new_height = int(src_height * scale_factor)

        # Resize the source image
        resized_src_img = self.photo.resize((new_width, new_height), Resampling.LANCZOS)

        if self.render_inside:
            # Center the image if rendering inside
            paste_x = (image.width - new_width) // 2
            paste_y = (image.height - new_height) // 2
        else:
            # Calculate cropping positions based on crop_bias
            crop_bias_x = crop_bias / 100.0
            crop_bias_y = crop_bias / 100.0

            # Calculate the crop box considering the bias
            crop_box_x1 = max(0, int((new_width - image.width) * crop_bias_x))
            crop_box_y1 = max(0, int((new_height - image.height) * crop_bias_y))
            crop_box_x2 = crop_box_x1 + image.width
            crop_box_y2 = crop_box_y1 + image.height

            # Crop the resized image to fit the destination image exactly
            resized_src_img = resized_src_img.crop((crop_box_x1, crop_box_y1, crop_box_x2, crop_box_y2))

            # Set paste_x and paste_y to (0,0) since we're filling the image fully
            paste_x, paste_y = 0, 0

        # Paste the resized or cropped image onto the destination image
        image.paste(resized_src_img, (paste_x, paste_y))

        return image


def correct_image_orientation(image: Image) -> Image:
    # Try to get the orientation tag from EXIF data
    try:
        orientation = 0
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == 'Orientation':
                break
        exif = image.getexif()

        if exif is not None:
            orientation = exif.get(orientation, 1)

            # Apply the necessary rotation or flipping based on the orientation value
            if orientation == 3:
                image = image.rotate(180, expand=True)
            elif orientation == 6:
                image = image.rotate(270, expand=True)
            elif orientation == 8:
                image = image.rotate(90, expand=True)
            elif orientation == 2:
                image = image.transpose(Transpose.FLIP_LEFT_RIGHT)
            elif orientation == 4:
                image = image.transpose(Transpose.FLIP_TOP_BOTTOM)
            elif orientation == 5:
                image = image.transpose(Transpose.FLIP_LEFT_RIGHT).rotate(270, expand=True)
            elif orientation == 7:
                image = image.transpose(Transpose.FLIP_LEFT_RIGHT).rotate(90, expand=True)

    except (AttributeError, KeyError, IndexError):
        # If there's no EXIF data or an error occurs, the image orientation is assumed to be normal
        pass

    return image

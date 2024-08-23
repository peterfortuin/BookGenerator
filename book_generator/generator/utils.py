from typing import Callable

from PIL import Image, ExifTags
from PIL.Image import Transpose


def draw_on_region(
        image: Image,
        left: float, top: float, right: float, bottom: float,
        method: Callable[[Image], Image]) -> Image:
    # Ensure x1, y1, x2, y2 are within the range [0, 100]
    left = max(0.0, min(100.0, left))
    top = max(0.0, min(100.0, top))
    right = max(0.0, min(100.0, right))
    bottom = max(0.0, min(100.0, bottom))

    # Convert percentages to pixel values
    dst_width, dst_height = image.size
    left = int(left / 100 * dst_width)
    top = int(top / 100 * dst_height)
    right = int(right / 100 * dst_width)
    bottom = int(bottom / 100 * dst_height)

    box = (left, top, right, bottom)
    region: Image = image.crop(box)

    updated_region = method(region)

    image.paste(updated_region, box, updated_region)

    return image


transparent_color = (0, 0, 0, 0)


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

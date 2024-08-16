from typing import Callable

from PIL import Image


def draw_on_region(image: Image, left: int, top: int, right: int, bottom: int, method: Callable[[Image], Image]) -> Image:
    # Ensure x1, y1, x2, y2 are within the range [0, 100]
    left = max(0, min(100, left))
    top = max(0, min(100, top))
    right = max(0, min(100, right))
    bottom = max(0, min(100, bottom))

    # Convert percentages to pixel values
    dst_width, dst_height = image.size
    left = int(left / 100 * dst_width)
    top = int(top / 100 * dst_height)
    right = int(right / 100 * dst_width)
    bottom = int(bottom / 100 * dst_height)

    box = (left, top, right, bottom)
    region: Image = image.crop(box)

    updated_region = method(region)

    image.paste(updated_region, box)

    return image

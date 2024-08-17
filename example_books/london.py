from book_generator.generator.spread import Spread, TwoSinglePagesTemplateSpread, TwoPageTemplateSpread
from book_generator.generator.book import Book
from book_generator.generator.photo import Photo
from templates.double_page_templates.two_page_photo_template import TwoPagePhotoTemplate
from templates.single_page_templates.one_photo_template import OnePhotoTemplate


def get_book() -> Book:
    return Book(
        "London",
        29.8,
        30.1,
        TwoSinglePagesTemplateSpread(
            OnePhotoTemplate(Photo('https://unsplash.com/photos/jAj5yVH8Ooc/download?ixid=M3wxMjA3fDB8MXxzZWFyY2h8MTl8fGxvbmRvbnxlbnwwfHx8fDE3MjM0NTI2MTF8MA&force=true&w=640')),
            OnePhotoTemplate(Photo('https://unsplash.com/photos/g-krQzQo9mI/download?ixid=M3wxMjA3fDB8MXxzZWFyY2h8Mnx8bG9uZG9ufGVufDB8fHx8MTcyMzQ1MjYxMXww&force=true&w=640'))
        ),
        TwoPageTemplateSpread(
            TwoPagePhotoTemplate(Photo('https://unsplash.com/photos/GlQBrIRmaJg/download?ixid=M3wxMjA3fDB8MXxzZWFyY2h8OHx8bG9uZG9uJTIwcGFub3JhbWljfGVufDB8fHx8MTcyMzgxNTMwOHww&force=true&w=640', render_inside=False, crop_bias=50))
        )
    )

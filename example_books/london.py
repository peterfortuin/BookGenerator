from book_generator.data_model.page import Page
from book_generator.data_model.book import Book
from book_generator.data_model.photo import Photo


def get_book() -> Book:
    return Book(
        Page(
            Photo('https://unsplash.com/photos/jAj5yVH8Ooc/download?ixid=M3wxMjA3fDB8MXxzZWFyY2h8MTl8fGxvbmRvbnxlbnwwfHx8fDE3MjM0NTI2MTF8MA&force=true&w=640')
        ),
        Page(
            Photo('https://unsplash.com/photos/g-krQzQo9mI/download?ixid=M3wxMjA3fDB8MXxzZWFyY2h8Mnx8bG9uZG9ufGVufDB8fHx8MTcyMzQ1MjYxMXww&force=true&w=640'),
            Photo('https://unsplash.com/photos/Oja2ty_9ZLM/download?ixid=M3wxMjA3fDB8MXxzZWFyY2h8NHx8bG9uZG9ufGVufDB8fHx8MTcyMzQ1MjYxMXww&force=true&w=640'),
            Photo('https://unsplash.com/photos/mOEqOtmuPG8/download?ixid=M3wxMjA3fDB8MXxzZWFyY2h8Nnx8bG9uZG9ufGVufDB8fHx8MTcyMzQ1MjYxMXww&force=true&w=640'),
        )
    )

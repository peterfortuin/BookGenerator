import argparse

import uvicorn
from dependency_injector.wiring import inject, Provide, register_loader_containers

from containers.book_generator_container import BookGeneratorContainer, book_generator_container
from services.book_service import BookService
from web.web import fast_api


@inject
def main(book_service: BookService = Provide[BookGeneratorContainer.book_service]):
    args = argument_parser()

    book_service.set_book_script(args.bookscript)

    uvicorn.run(fast_api, host="127.0.0.1", port=8000)


def argument_parser():
    parser = argparse.ArgumentParser(description="Book generator")
    parser.add_argument("bookscript", type=str, help="Path to script that describes the book to render.")
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    book_generator_container.wire(
        modules=[
            __name__,
            "web.web"
        ]
    )
    register_loader_containers(book_generator_container)

    main()

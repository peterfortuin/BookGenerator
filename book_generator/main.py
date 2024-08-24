import argparse

import uvicorn
from dependency_injector.wiring import inject, Provide, register_loader_containers

from book_generator.web import fast_api
from containers.book_generator_container import BookGeneratorContainer
from services.book_service import BookService


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
    container = BookGeneratorContainer()
    container.wire(modules=[__name__])
    register_loader_containers(container)

    main()

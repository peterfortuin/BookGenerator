import argparse
import importlib
import sys

import uvicorn

from book_generator.web import fast_api


def main():
    parser = argparse.ArgumentParser(description="Book generator")
    parser.add_argument("bookscript", type=str, help="Path to script that describes the book to render.")
    args = parser.parse_args()

    script = load_script(args.bookscript)

    book = script.get_book()
    book.render_all_spreads()

    uvicorn.run(fast_api, host="127.0.0.1", port=8000)


def load_script(bookscript):
    spec = importlib.util.spec_from_file_location("book_generator.script", bookscript)
    module = importlib.util.module_from_spec(spec)
    sys.modules["book_generator.script"] = module
    spec.loader.exec_module(module)

    return module


if __name__ == "__main__":
    main()

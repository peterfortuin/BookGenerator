import argparse
import importlib
import sys


def main():
    parser = argparse.ArgumentParser(description="Book generator")
    parser.add_argument("bookscript", type=str, help="Path to script that describes the book to render.")
    args = parser.parse_args()

    script = load_script(args)

    book = script.get_book()


def load_script(args):
    spec = importlib.util.spec_from_file_location("book_generator.script", args.bookscript)
    module = importlib.util.module_from_spec(spec)
    sys.modules["book_generator.script"] = module
    spec.loader.exec_module(module)

    return module


if __name__ == "__main__":
    main()

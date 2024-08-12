import argparse


def main():
    parser = argparse.ArgumentParser(description="Book generator")
    parser.add_argument("bookscript", type=str, help="Path to script that describes the book to render.")
    args = parser.parse_args()

    with open(args.bookscript) as file:
        exec(file.read())


if __name__ == "__main__":
    main()

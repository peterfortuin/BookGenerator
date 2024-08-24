import importlib
import sys
from typing import Optional


class BookService:
    def __init__(self):
        self._book_script: Optional[str] = None
        self.script_module: Optional[str] = None

    def set_book_script(self, book_script: str):
        self._book_script = book_script

        self.script_module = self.load_script(self._book_script)

        book = self.script_module.get_book()
        book.render_all_spreads()

    @staticmethod
    def load_script(book_script):
        spec = importlib.util.spec_from_file_location("book_generator.script", book_script)
        module = importlib.util.module_from_spec(spec)
        sys.modules["book_generator.script"] = module
        spec.loader.exec_module(module)

        return module

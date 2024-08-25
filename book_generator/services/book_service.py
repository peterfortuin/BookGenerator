import importlib
import sys
import types
from typing import Optional

from generator.book import Book


class ScriptModuleInterface(types.ModuleType):
    def get_book(self) -> Book:
        pass


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
    def load_script(book_script) -> ScriptModuleInterface:
        spec = importlib.util.spec_from_file_location("book_generator.script", book_script)
        module = importlib.util.module_from_spec(spec)
        sys.modules["book_generator.script"] = module
        spec.loader.exec_module(module)

        return module

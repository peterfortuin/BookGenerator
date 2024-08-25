import importlib
import sys
import types
from typing import Optional

from generator.book import Book
from utils.filewatcher import FileWatcher


class ScriptModuleInterface(types.ModuleType):
    def get_book(self) -> Book:
        pass


class BookService:
    def __init__(self):
        self._book_script: Optional[str] = None
        self._script_module: Optional[ScriptModuleInterface] = None
        self._script_watcher: Optional[FileWatcher] = None

    def set_book_script(self, book_script: str):
        if self._script_watcher is not None:
            self._script_watcher.stop()

        self._book_script = book_script

        self._script_module = self._load_script()

        self.generate_book()

        self._script_watcher = FileWatcher(self._book_script, self._reload_script)
        self._script_watcher.start()

    def generate_book(self):
        book = self._script_module.get_book()
        book.render_all_spreads()

    def _load_script(self) -> ScriptModuleInterface:
        spec = importlib.util.spec_from_file_location("book_generator.script", self._book_script)
        module = importlib.util.module_from_spec(spec)
        sys.modules["book_generator.script"] = module
        spec.loader.exec_module(module)

        return module

    def _reload_script(self):
        self._script_module = self._load_script()
        self.generate_book()

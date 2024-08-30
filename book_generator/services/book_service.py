import importlib
import sys
import types
from typing import Optional, Dict

from generator.book import Book
from utils.asyncio_thread import AsyncioThread
from utils.filewatcher import FileWatcher


class ScriptModuleInterface(types.ModuleType):
    def get_book(self) -> Book:
        pass


class BookService:
    def __init__(self):
        self._book_script: Optional[str] = None
        self._script_module: Optional[ScriptModuleInterface] = None
        self._script_watcher: Optional[FileWatcher] = None
        self._book: Optional[Book] = None
        self._thread = AsyncioThread()
        self._thread.start()

    def set_book_script(self, book_script: str):
        if self._script_watcher is not None:
            self._script_watcher.stop()

        self._book_script = book_script

        self._script_module = self._load_script()

        self.generate_book()

        self._script_watcher = FileWatcher(self._book_script, self._reload_script)
        self._script_watcher.start()

    def generate_book(self):
        self._book = self._script_module.get_book()

        self._thread.schedule_task(self._book.render_all_spreads())



    def _load_script(self) -> ScriptModuleInterface:
        spec = importlib.util.spec_from_file_location("book_generator.script", self._book_script)
        module = importlib.util.module_from_spec(spec)
        sys.modules["book_generator.script"] = module
        spec.loader.exec_module(module)

        return module

    def _reload_script(self):
        self._script_module = self._load_script()
        self.generate_book()

    def get_number_of_pages(self) -> int:
        return self._book.get_number_of_pages()

    def get_render_dir(self) -> str:
        return self._book.get_render_dir()

    async def wait_until_event(self) -> Dict[str, str]:
        return await self._book.wait_until_event()

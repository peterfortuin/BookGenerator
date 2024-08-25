from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
from watchdog.observers.polling import PollingObserver


class FileWatcher:
    def __init__(self, file_path: str, callback):
        self.file_path = file_path
        self.callback = callback
        self.observer = PollingObserver()

    def start(self):
        event_handler = FileSystemEventHandler()
        event_handler.on_modified = self.on_modified

        self.observer.schedule(event_handler, self.file_path, recursive=False)
        self.observer.start()

    def on_modified(self, event):
        if event.src_path == self.file_path:
            self.callback()

    def stop(self):
        self.observer.stop()
        self.observer.join()

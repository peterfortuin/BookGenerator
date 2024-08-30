import asyncio
import threading


class AsyncioThread(threading.Thread):
    def __init__(self):
        super().__init__()
        self._loop = None
        self._tasks = asyncio.Queue()

    def run(self):
        self._loop = asyncio.new_event_loop()
        self._loop.set_debug(True)
        asyncio.set_event_loop(self._loop)
        self._loop.run_until_complete(self._run_tasks())

    async def _run_tasks(self):
        while True:
            task = await self._tasks.get()
            if task is None:
                break
            await task

    def schedule_task(self, coro):
        asyncio.run_coroutine_threadsafe(self._tasks.put(coro), self._loop)

    def stop(self):
        self.schedule_task(self._stop_loop())

    async def _stop_loop(self):
        self._loop.stop()

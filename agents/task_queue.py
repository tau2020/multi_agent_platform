# agents/task_queue.py

import asyncio
import logging
from typing import Callable, Any

class TaskQueue:
    def __init__(self):
        self.task_queue = asyncio.Queue()
        self.result_queue = asyncio.Queue()
        self.workers = []
        self.stop_event = asyncio.Event()
        self.logger = logging.getLogger(self.__class__.__name__)

    async def add_task(self, task: Callable[..., Any], *args, **kwargs):
        await self.task_queue.put((task, args, kwargs))

    async def get_result(self):
        return await self.result_queue.get()

    async def worker(self, worker_id: int):
        while not self.stop_event.is_set():
            try:
                task, args, kwargs = await asyncio.wait_for(self.task_queue.get(), timeout=1)
                if asyncio.iscoroutinefunction(task):
                    result = await task(*args, **kwargs)
                else:
                    result = task(*args, **kwargs)
                await self.result_queue.put(result)
                self.task_queue.task_done()
            except asyncio.TimeoutError:
                continue
            except Exception as e:
                self.logger.error(f"An error occurred in worker {worker_id}: {e}")
                self.task_queue.task_done()

    async def start_workers(self, num_workers: int):
        for i in range(num_workers):
            task = asyncio.create_task(self.worker(i))
            self.workers.append(task)

    async def stop_workers(self):
        self.stop_event.set()
        await asyncio.gather(*self.workers, return_exceptions=True)
        self.workers.clear()

    async def wait_completion(self):
        await self.task_queue.join()

# agents/task_queue.py

import queue
import threading
from typing import Callable

class TaskQueue:
    def __init__(self):
        self.task_queue = queue.Queue()
        self.result_queue = queue.Queue()
        self.workers = []
        self.stop_event = threading.Event()

    def add_task(self, task: Callable, *args, **kwargs):
        self.task_queue.put((task, args, kwargs))

    def get_result(self):
        return self.result_queue.get()

    def worker(self):
        while not self.stop_event.is_set():
            try:
                task, args, kwargs = self.task_queue.get(timeout=1)
                result = task(*args, **kwargs)
                self.result_queue.put(result)
                self.task_queue.task_done()
            except queue.Empty:
                continue
            except Exception as e:
                print(f"An error occurred in worker: {e}")
                self.task_queue.task_done()

    def start_workers(self, num_workers: int):
        for _ in range(num_workers):
            t = threading.Thread(target=self.worker)
            t.start()
            self.workers.append(t)

    def stop_workers(self):
        self.stop_event.set()
        for worker in self.workers:
            worker.join()
        self.workers.clear()

    def wait_completion(self):
        self.task_queue.join()

task_queue = TaskQueue()

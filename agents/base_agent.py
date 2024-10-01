# agents/base_agent.py

import asyncio
import logging
from abc import ABC, abstractmethod
from typing import Any, Dict

class BaseAgent(ABC):
    def __init__(self, agent_id: str, input_queue: asyncio.Queue, output_queue: asyncio.Queue):
        self.agent_id = agent_id
        self.input_queue = input_queue
        self.output_queue = output_queue
        self.logger = logging.getLogger(f'{self.__class__.__name__}-{self.agent_id}')

    async def run(self):
        self.logger.info(f"Agent {self.agent_id} started.")
        while True:
            try:
                message = await asyncio.wait_for(self.input_queue.get(), timeout=1)
                if message.get('type') == 'terminate':
                    self.logger.info(f"Agent {self.agent_id} terminating.")
                    break
                result = await self.work_on_task(message)
                await self.output_queue.put({
                    'type': 'task_completed',
                    'task_id': message['id'],
                    'agent_id': self.agent_id,
                    'result': result
                })
            except asyncio.TimeoutError:
                continue
            except Exception as e:
                self.logger.error(f"An error occurred: {e}")

    @abstractmethod
    async def work_on_task(self, task: Dict[str, Any]) -> Any:
        pass

    async def submit_output(self, task_id: str, content: Any):
        await self.output_queue.put({
            'type': 'task_completed',
            'task_id': task_id,
            'agent_id': self.agent_id,
            'result': content
        })

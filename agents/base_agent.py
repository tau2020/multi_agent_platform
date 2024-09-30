import asyncio
import logging
import os
from .model_loader import get_llm

class BaseAgent:
    def __init__(self, agent_id, input_queue, output_queue, model_type='openai'):
        self.agent_id = agent_id
        self.input_queue = input_queue
        self.output_queue = output_queue
        self.model_type = model_type
        self.llm_model = self.load_model()
        self.logger = logging.getLogger(f'{self.__class__.__name__}-{self.agent_id}')
        self.task_semaphore = asyncio.Semaphore(5)  # Limit concurrent tasks

    def load_model(self):
        config = {
            'OPENAI_API_KEY': os.getenv('OPENAI_API_KEY'),
            'ANTHROPIC_API_KEY': os.getenv('ANTHROPIC_API_KEY'),
            'HUGGINGFACE_MODEL_NAME': os.getenv('HUGGINGFACE_MODEL_NAME'),
        }
        return get_llm(self.model_type, config)

    async def run(self):
        self.logger.info(f"Agent {self.agent_id} started.")
        while True:
            try:
                message = await asyncio.wait_for(self.input_queue.get(), timeout=1)
                if message.msg_type == 'terminate':
                    self.logger.info(f"Agent {self.agent_id} terminating.")
                    break
                asyncio.create_task(self.process_task(message))
            except asyncio.TimeoutError:
                continue
            except Exception as e:
                self.logger.error(f"An error occurred: {e}")

    async def process_task(self, message):
        raise NotImplementedError("Subclasses must implement this method")

    async def submit_output(self, task_id, content):
        output_message = {
            'sender': self.agent_id,
            'receiver': 'monitor_agent',
            'msg_type': 'task_completed',
            'content': {
                'task_id': task_id,
                'output': content,
            }
        }
        await self.output_queue.put(output_message)
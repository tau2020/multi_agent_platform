# agents/agent_middleware.py

import asyncio
import logging
import os
from .model_loader import get_llm
from .message import Message
from dotenv import load_dotenv

load_dotenv()

class MiddlewareAgent:
    def __init__(self, agent_id, input_queue, output_queue, model_type='openai'):
        self.agent_id = agent_id
        self.agent_type = 'middleware'
        self.input_queue = input_queue
        self.output_queue = output_queue
        self.model_type = model_type
        self.llm_model = self.load_model()
        self.logger = logging.getLogger(f'MiddlewareAgent-{self.agent_id}')

    def load_model(self):
        config = {
            'OPENAI_API_KEY': os.getenv('OPENAI_API_KEY'),
            'ANTHROPIC_API_KEY': os.getenv('ANTHROPIC_API_KEY'),
            'HUGGINGFACE_MODEL_NAME': os.getenv('HUGGINGFACE_MODEL_NAME'),
        }
        return get_llm(self.model_type, config)

    async def run(self):
        self.logger.info("Agent started.")
        while True:
            try:
                message = await asyncio.wait_for(self.input_queue.get(), timeout=1)
                if message.msg_type == 'task':
                    await self.work_on_task(message.content)
                elif message.msg_type == 'terminate':
                    self.logger.info("Terminating agent.")
                    break
            except asyncio.TimeoutError:
                continue
            except Exception as e:
                self.logger.error(f"An error occurred: {e}")
                break

    async def work_on_task(self, task):
        self.logger.info(f"Received task: {task['id']}")
        integration_code = await self.integrate_components(task['frontend_code'], task['backend_code'])
        await self.submit_output(task['id'], integration_code)
        self.logger.info(f"Completed task: {task['id']}")

    async def integrate_components(self, frontend_code, backend_code):
        prompt = (
            f"As a middleware developer, integrate the following Angular front-end code with the Node.js back-end code. "
            f"Ensure that the front-end correctly communicates with the back-end APIs, and all endpoints are properly connected.\n\n"
            f"Front-End Code:\n{frontend_code}\n\n"
            f"Back-End Code:\n{backend_code}\n\n"
            "Provide any necessary modifications or notes to ensure seamless integration."
        )
        integration_notes = await asyncio.get_event_loop().run_in_executor(None, self.llm_model.generate, prompt)
        integrated_code = {
            'frontend_code': frontend_code,
            'backend_code': backend_code,
            'integration_notes': integration_notes
        }
        self.logger.debug(f"Integration notes: {integration_notes}")
        return integrated_code

    async def submit_output(self, task_id, code):
        output_message = Message(
            sender=self.agent_id,
            receiver='monitor_agent',
            msg_type='integration_output',
            content={
                'task_id': task_id,
                'code': code,
                'type': 'integration'
            }
        )
        await self.output_queue.put(output_message)

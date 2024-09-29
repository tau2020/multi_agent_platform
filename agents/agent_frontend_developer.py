# agents/agent_frontend_developer.py

import asyncio
import logging
import os
from .model_loader import get_llm
from .message import Message
from dotenv import load_dotenv

load_dotenv()

class FrontEndDeveloperAgent:
    def __init__(self, agent_id, input_queue, output_queue, model_type='openai'):
        self.agent_id = agent_id
        self.agent_type = 'frontend'
        self.specialization = 'Angular'
        self.input_queue = input_queue
        self.output_queue = output_queue
        self.model_type = model_type
        self.llm_model = self.load_model()
        self.logger = logging.getLogger(f'FrontEndDeveloperAgent-{self.agent_id}')

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
        component_code = await self.generate_component(task['description'])
        await self.submit_output(task['id'], component_code)
        self.logger.info(f"Completed task: {task['id']}")

    async def generate_component(self, description):
        prompt = (
            f"Write clean, well-documented Angular (TypeScript) code to accomplish the following task:\n\n"
            f"{description}\n\n"
            "Ensure that the code follows Angular best practices, includes necessary imports, "
            "and does not include any extraneous print statements or console logs."
        )
        code = await asyncio.get_event_loop().run_in_executor(None, self.llm_model.generate, prompt)
        self.logger.debug(f"Generated code: {code}")
        return code

    async def submit_output(self, task_id, code):
        output_message = Message(
            sender=self.agent_id,
            receiver='monitor_agent',
            msg_type='output',
            content={
                'task_id': task_id,
                'code': code,
                'type': 'frontend'
            }
        )
        await self.output_queue.put(output_message)

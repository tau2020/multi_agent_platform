import asyncio
import logging
import os
from agents.model_loader import get_llm
from dotenv import load_dotenv

load_dotenv()

class DeveloperAgent:
    def __init__(self, agent_id, input_queue, output_queue, model_type='openai'):
        self.agent_id = agent_id
        self.input_queue = input_queue
        self.output_queue = output_queue
        self.model_type = model_type
        self.llm_model = self.load_model()
        self.logger = logging.getLogger(f'DeveloperAgent-{self.agent_id}')

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
                if isinstance(message, dict):
                    if message.get('type') == 'terminate':
                        self.logger.info("Terminating agent.")
                        break
                    await self.work_on_task(message)
                else:
                    self.logger.warning(f"Received unexpected message type: {type(message)}")
            except asyncio.TimeoutError:
                continue
            except Exception as e:
                self.logger.error(f"An error occurred: {e}")

    async def work_on_task(self, task):
        task_id = task.get('id')
        description = task.get('description')
        self.logger.info(f"Working on task: {task_id}")
        
        # Generate code based on the task description
        code = await self.generate_code(description)
        
        # Submit the result
        await self.submit_output(task_id, code)
        
        self.logger.info(f"Completed task: {task_id}")

    async def generate_code(self, description):
        prompt = (
            f"Write clean, well-documented code to accomplish the following task:\n\n"
            f"{description}\n\n"
            "Ensure that the code follows best practices and includes necessary comments."
        )
        code = await asyncio.get_event_loop().run_in_executor(None, self.llm_model.generate, prompt)
        return code

    async def submit_output(self, task_id, code):
        output_message = {
            'task_id': task_id,
            'code': code,
            'agent_id': self.agent_id,
            'type': 'task_completed'
        }
        await self.output_queue.put(output_message)
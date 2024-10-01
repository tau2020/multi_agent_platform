# agents/agent_developer.py

import asyncio
import logging
from agents.base_agent import BaseAgent
from typing import Dict, Any

class DeveloperAgent(BaseAgent):
    def __init__(self, agent_id: str, input_queue: asyncio.Queue, output_queue: asyncio.Queue, llm: Any, role: str = 'developer'):
        super().__init__(agent_id, input_queue, output_queue)
        self.llm = llm
        self.role = role
        self.logger = logging.getLogger(f'DeveloperAgent-{self.role}-{self.agent_id}')

    async def work_on_task(self, task: Dict[str, Any]) -> str:
        self.logger.info(f"Working on task: {task['id']} with role: {self.role}")
        if self.role == 'function_definer':
            content = await self.define_function(task['description'])
        elif self.role == 'logic_implementer':
            content = await self.implement_logic(task['description'])
        elif self.role == 'tester':
            content = await self.test_function(task['description'])
        elif self.role == 'documenter':
            content = await self.document_function(task['description'])
        else:
            content = await self.generate_code(task['description'])
        await self.submit_output(task['id'], content)
        self.logger.info(f"Completed task: {task['id']} with role: {self.role}")
        return content

    async def define_function(self, description: str) -> str:
        prompt = f"""
        Define a function for the following task:
        
        Task: {description}
        
        Provide a function signature with appropriate parameters.
        """
        try:
            code = await asyncio.get_event_loop().run_in_executor(None, self.llm.generate, prompt)
            if not code.strip():
                raise ValueError("LLM returned an empty response")
            return code
        except Exception as e:
            self.logger.error(f"Failed to define function: {e}")
            raise

    async def implement_logic(self, description: str) -> str:
        prompt = f"""
        Implement the logic for the following function:
        
        Task: {description}
        
        Write the body of the function to perform the required operation.
        """
        try:
            code = await asyncio.get_event_loop().run_in_executor(None, self.llm.generate, prompt)
            if not code.strip():
                raise ValueError("LLM returned an empty response")
            return code
        except Exception as e:
            self.logger.error(f"Failed to implement logic: {e}")
            raise

    async def test_function(self, description: str) -> str:
        prompt = f"""
        Write test cases for the following function:
        
        Task: {description}
        
        Ensure to cover edge cases and typical usage scenarios.
        """
        try:
            tests = await asyncio.get_event_loop().run_in_executor(None, self.llm.generate, prompt)
            if not tests.strip():
                raise ValueError("LLM returned an empty response")
            return tests
        except Exception as e:
            self.logger.error(f"Failed to write tests: {e}")
            raise

    async def document_function(self, description: str) -> str:
        prompt = f"""
        Document the following function:
        
        Task: {description}
        
        Provide docstrings and inline comments explaining the purpose and functionality.
        """
        try:
            documentation = await asyncio.get_event_loop().run_in_executor(None, self.llm.generate, prompt)
            if not documentation.strip():
                raise ValueError("LLM returned an empty response")
            return documentation
        except Exception as e:
            self.logger.error(f"Failed to document function: {e}")
            raise

    async def generate_code(self, description: str) -> str:
        prompt = f"""
        Write clean, well-documented code to accomplish the following task:
        
        {description}
        
        Ensure that the code follows best practices and includes necessary comments.
        Wrap the code in a deployable function or class.
        """
        try:
            code = await asyncio.get_event_loop().run_in_executor(None, self.llm.generate, prompt)
            if not code.strip():
                raise ValueError("LLM returned an empty response")
            return code
        except Exception as e:
            self.logger.error(f"Failed to generate code: {e}")
            raise

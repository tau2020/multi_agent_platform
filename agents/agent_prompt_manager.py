# agents/prompt_manager.py

import asyncio
import logging
from typing import Any, Dict
from agents.agent_developer import DeveloperAgent
import uuid

class PromptManager:
    def __init__(self, output_queue: asyncio.Queue):
        self.output_queue = output_queue
        self.logger = logging.getLogger(self.__class__.__name__)
        self.agents = {}

    async def assign_role_and_delegate(self, subtask: Dict[str, Any], output_queue: asyncio.Queue, llm: Any):
        role = self.determine_role(subtask)
        agent_id = f"{role}_agent_{uuid.uuid4()}"
        agent = DeveloperAgent(agent_id, asyncio.Queue(), output_queue, llm, role=role)
        self.agents[agent_id] = agent
        asyncio.create_task(agent.run())
        await agent.input_queue.put(subtask)
        self.logger.info(f"Assigned role '{role}' to agent '{agent_id}' for subtask '{subtask['id']}'")

    def determine_role(self, subtask: Dict[str, Any]) -> str:
        description = subtask.get('description', '').lower()
        if 'define' in description or 'create' in description:
            return 'function_definer'
        elif 'implement' in description or 'logic' in description:
            return 'logic_implementer'
        elif 'test' in description:
            return 'tester'
        elif 'document' in description:
            return 'documenter'
        else:
            return 'developer'

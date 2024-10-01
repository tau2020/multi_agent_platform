# agents/task_processing_agent.py

import os
import json
from typing import Dict, Any
import asyncio
import aiofiles

class TaskProcessingAgent:
    def __init__(self, agent_id: str, input_queue: asyncio.Queue, output_queue: asyncio.Queue, model_type: str = 'openai'):
        self.agent_id = agent_id
        self.input_queue = input_queue
        self.output_queue = output_queue
        self.model_type = model_type
        self.tasks_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tasks')

    async def work_on_task(self, task: Dict[str, Any]) -> str:
        if not isinstance(task, dict):
            return f"Error: Expected task to be a dictionary, but got {type(task)}"

        task_id = task.get('task_id')
        if not task_id:
            return "Error: Task is missing 'task_id'"

        task_file = os.path.join(self.tasks_dir, f"{task_id}_task.json")

        if not os.path.exists(task_file):
            return f"Error: Task file for {task_id} not found."

        try:
            async with aiofiles.open(task_file, 'r') as f:
                task_data = json.loads(await f.read())
        except json.JSONDecodeError:
            return f"Error: Failed to parse task file for {task_id}"

        if not isinstance(task_data, dict):
            return f"Error: Task data for {task_id} is not a dictionary"

        if task_data.get('status') != 'assigned':
            return f"{self.agent_id}: Task {task_id} status is '{task_data.get('status')}'. Skipping."

        print(f"{self.agent_id} is working on Task ID: {task_id}")

        try:
            result = await self.process_task(task_data)

            task_data['status'] = 'processed'
            async with aiofiles.open(task_file, 'w') as f:
                await f.write(json.dumps(task_data, indent=2))

            if self.output_queue:
                await self.output_queue.put((task_id, result))

            return f"{self.agent_id}: Task {task_id} processing complete."
        except Exception as e:
            return f"{self.agent_id}: Error processing task {task_id}: {str(e)}"

    async def process_task(self, task_data: Dict[str, Any]) -> str:
        raise NotImplementedError("Subclasses must implement this method")

    async def generate_content(self, description: str) -> str:
        raise NotImplementedError("Subclasses must implement this method")

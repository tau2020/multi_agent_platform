import asyncio
from collections import deque
from .output_manager import OutputManager

class WorkflowManager:
    def __init__(self, monitor_agent, output_manager=None):
        self.monitor_agent = monitor_agent
        self.task_queue = asyncio.Queue()
        self.completed_tasks = set()
        self.current_workflow = None
        self.total_tasks = 0
        self.output_manager = output_manager  # Use provided OutputManager instance

    async def execute_workflow(self, workflow):
        self.current_workflow = workflow
        tasks = workflow['tasks']
        self.total_tasks = len(tasks)
        task_dict = {task['id']: task for task in tasks}
        
        self.output_manager.log_system_event(f"Starting workflow execution. Total tasks: {self.total_tasks}")
        
        for task in tasks:
            if not task['dependencies']:
                await self.task_queue.put(task)

        while len(self.completed_tasks) < self.total_tasks:
            if not self.task_queue.empty():
                task = await self.task_queue.get()
                await self.monitor_agent.assign_task(task)
            else:
                await asyncio.sleep(0.1)

        self.output_manager.log_system_event("All tasks in the workflow have been completed.")
        return True

    async def task_completed(self, task_id):
        self.completed_tasks.add(task_id)
        self.output_manager.log_task_event(
            task_id, 
            "completed", 
            f"Progress: {len(self.completed_tasks)}/{self.total_tasks}"
        )
        
        for task in self.current_workflow['tasks']:
            if task['id'] not in self.completed_tasks and \
               all(dep in self.completed_tasks for dep in task['dependencies']):
                await self.task_queue.put(task)
        
        if len(self.completed_tasks) == self.total_tasks:
            self.output_manager.log_system_event("All tasks have been completed. Initiating graceful shutdown.")
            await self.monitor_agent.initiate_shutdown()

    # Remove get_output_json and save_output_to_file methods as they are handled by OutputManager

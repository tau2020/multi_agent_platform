import asyncio
import logging
from agents.agent_developer import DeveloperAgent

class MonitorAgent:
    def __init__(self, model_type='openai'):
        self.input_queue = asyncio.Queue()
        self.output_queue = asyncio.Queue()
        self.agents = {}
        self.task_queue = asyncio.Queue()
        self.completed_tasks = set()
        self.model_type = model_type
        self.logger = logging.getLogger('MonitorAgent')

    async def run(self):
        self.logger.info("Monitor Agent started.")
        await self.start_agents()
        while True:
            try:
                message = await asyncio.wait_for(self.input_queue.get(), timeout=1)
                if isinstance(message, dict):
                    if message.get('type') == 'new_task':
                        await self.assign_task(message)
                    elif message.get('type') == 'task_completed':
                        await self.process_completed_task(message)
                    elif message.get('type') == 'terminate':
                        break
                else:
                    self.logger.warning(f"Received unexpected message type: {type(message)}")
            except asyncio.TimeoutError:
                continue
            except Exception as e:
                self.logger.error(f"An error occurred: {e}")

    async def start_agents(self):
        for i in range(5):  # Start 5 developer agents
            agent_id = f'dev_agent_{i}'
            agent_input_queue = asyncio.Queue()
            agent = DeveloperAgent(agent_id, agent_input_queue, self.output_queue, self.model_type)
            self.agents[agent_id] = {'agent': agent, 'queue': agent_input_queue}
            asyncio.create_task(agent.run())
        self.logger.info(f"Started {len(self.agents)} developer agents")

    async def assign_task(self, task):
        task_id = task['id']
        self.logger.info(f"Received new task: {task_id}")
        await self.task_queue.put(task)
        await self.distribute_tasks()

    async def distribute_tasks(self):
        while not self.task_queue.empty():
            task = await self.task_queue.get()
            assigned = False
            for agent_id, agent_info in self.agents.items():
                if agent_info['queue'].qsize() == 0:
                    await agent_info['queue'].put(task)
                    self.logger.info(f"Assigned task {task['id']} to {agent_id}")
                    assigned = True
                    break
            if not assigned:
                await self.task_queue.put(task)
                break

    async def process_completed_task(self, message):
        task_id = message['task_id']
        self.completed_tasks.add(task_id)
        self.logger.info(f"Task {task_id} completed by {message['agent_id']}")
        await self.distribute_tasks()

    def stop(self):
        for agent_info in self.agents.values():
            agent_info['queue'].put_nowait({'type': 'terminate'})

    async def log_status(self):
        self.logger.info("Current system status:")
        self.logger.info(f"  Tasks in queue: {self.task_queue.qsize()}")
        self.logger.info(f"  Completed tasks: {len(self.completed_tasks)}")
        for agent_id, agent_info in self.agents.items():
            self.logger.info(f"  {agent_id} queue size: {agent_info['queue'].qsize()}")
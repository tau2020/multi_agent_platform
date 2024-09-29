# agents/agent_monitor.py

import asyncio
import logging
from .agent_frontend_developer import FrontEndDeveloperAgent
from .agent_backend_developer import BackEndDeveloperAgent
from .agent_middleware import MiddlewareAgent
from .agent_devops import DevOpsAgent
from .agent_tester import TesterAgent
from .agent_qa import QAAgent
from .message import Message

class MonitorAgent:
    def __init__(self, model_type='openai'):
        self.input_queue = asyncio.Queue()
        self.output_queue = asyncio.Queue()
        self.agents = {}
        self.task_counter = 0
        self.outputs = {}
        self.model_type = model_type
        self.logger = logging.getLogger('MonitorAgent')
        self.loop = asyncio.get_event_loop()

    async def run(self):
        self.logger.info("Monitor Agent started.")
        await self.start_agents()
        while True:
            try:
                message = await asyncio.wait_for(self.output_queue.get(), timeout=1)
                if message.msg_type == 'output':
                    await self.receive_output(message)
                elif message.msg_type == 'integration_output':
                    await self.receive_integrated_output(message)
                elif message.msg_type == 'terminate':
                    self.logger.info("Terminating Monitor Agent.")
                    break
            except asyncio.TimeoutError:
                continue
            except Exception as e:
                self.logger.error(f"An error occurred: {e}")
                break

    async def start_agents(self):
        await self.add_agent('frontend', 'frontend_agent_1')
        await self.add_agent('backend', 'backend_agent_1')
        await self.add_agent('middleware', 'middleware_agent_1')
        await self.add_agent('tester', 'tester_agent_1')
        await self.add_agent('qa', 'qa_agent_1')
        await self.add_agent('devops', 'devops_agent_1')

    async def add_agent(self, agent_type, agent_id):
        agent_input_queue = asyncio.Queue()
        agent = None
        if agent_type == 'frontend':
            agent = FrontEndDeveloperAgent(agent_id, agent_input_queue, self.input_queue, self.model_type)
        elif agent_type == 'backend':
            agent = BackEndDeveloperAgent(agent_id, agent_input_queue, self.input_queue, self.model_type)
        elif agent_type == 'middleware':
            agent = MiddlewareAgent(agent_id, agent_input_queue, self.input_queue, self.model_type)
        elif agent_type == 'tester':
            agent = TesterAgent(agent_id, agent_input_queue, self.input_queue, self.model_type)
        elif agent_type == 'qa':
            agent = QAAgent(agent_id, agent_input_queue, self.input_queue, self.model_type)
        elif agent_type == 'devops':
            agent = DevOpsAgent(agent_id, agent_input_queue, self.input_queue, self.model_type)
        else:
            self.logger.error(f"Unknown agent type: {agent_type}")
            return
        self.agents[agent_id] = agent
        self.loop.create_task(agent.run())
        self.logger.info(f"Added {agent_type} agent: {agent_id}")

    async def analyze_requirements(self, requirements):
        await self.decompose_tasks(requirements)

    async def decompose_tasks(self, requirements):
        frontend_description = f"Implement the following features: {', '.join(requirements['features'])}"
        backend_description = f"Develop APIs to support the following outputs: {', '.join(requirements['outputs'])}"
        frontend_task = {
            'id': self.generate_task_id(),
            'description': frontend_description,
            'type': 'frontend'
        }
        backend_task = {
            'id': self.generate_task_id(),
            'description': backend_description,
            'type': 'backend'
        }
        await self.assign_task('frontend', frontend_task)
        await self.assign_task('backend', backend_task)

    async def assign_task(self, agent_type, task):
        agent = self.get_available_agent(agent_type)
        if agent:
            message = Message(
                sender='monitor_agent',
                receiver=agent.agent_id,
                msg_type='task',
                content=task
            )
            await agent.input_queue.put(message)
            self.logger.info(f"Assigned task {task['id']} to {agent.agent_id}")
        else:
            self.logger.error(f"No available agent for task type: {agent_type}")

    def get_available_agent(self, agent_type):
        for agent in self.agents.values():
            if agent.agent_type == agent_type:
                return agent
        return None

    async def receive_output(self, message):
        output = message.content
        self.outputs[output['task_id']] = output
        self.logger.info(f"Received output from Agent {message.sender} for Task {output['task_id']}")
        if self.check_all_outputs_received():
            await self.integrate_outputs()

    def check_all_outputs_received(self):
        expected_tasks = 2
        return len(self.outputs) >= expected_tasks

    async def integrate_outputs(self):
        frontend_output = next((o for o in self.outputs.values() if o['type'] == 'frontend'), None)
        backend_output = next((o for o in self.outputs.values() if o['type'] == 'backend'), None)
        if frontend_output and backend_output:
            integration_task = {
                'id': self.generate_task_id(),
                'frontend_code': frontend_output['code'],
                'backend_code': backend_output['code'],
                'type': 'integration'
            }
            await self.assign_task('middleware', integration_task)
        else:
            self.logger.warning("Waiting for all outputs to proceed with integration.")

    async def receive_integrated_output(self, message):
        output = message.content
        self.logger.info(f"Received integrated output from Middleware Agent for Task {output['task_id']}")
        testing_task = {
            'id': self.generate_task_id(),
            'code': output,
            'type': 'testing'
        }
        await self.assign_task('tester', testing_task)
        await self.assign_task('qa', testing_task)

    async def terminate_agents(self):
        self.logger.info("Terminating all agents.")
        for agent in self.agents.values():
            message = Message(
                sender='monitor_agent',
                receiver=agent.agent_id,
                msg_type='terminate',
                content=None
            )
            await agent.input_queue.put(message)

    def generate_task_id(self):
        self.task_counter += 1
        return f"task_{self.task_counter}"

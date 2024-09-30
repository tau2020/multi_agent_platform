import asyncio
import logging
from agents.agent_monitor import MonitorAgent

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def simulate_tasks(monitor_agent, num_tasks=10):
    for i in range(num_tasks):
        task = {
            'type': 'new_task',
            'id': f'task_{i}',
            'description': f'Implement a function to calculate the factorial of {i}'
        }
        await monitor_agent.input_queue.put(task)
        logger.info(f"Submitted task_{i} to the system")
        await asyncio.sleep(0.5)  # Simulate some delay between task submissions

async def main():
    logger.info("Starting the Multi-Agent System")
    
    monitor_agent = MonitorAgent()
    monitor_task = asyncio.create_task(monitor_agent.run())
    
    logger.info("Simulating incoming tasks")
    await simulate_tasks(monitor_agent)
    
    logger.info("All tasks submitted. Waiting for completion...")
    
    # Allow some time for tasks to be processed
    for _ in range(10):
        await asyncio.sleep(5)
        await monitor_agent.log_status()
    
    # Stop the system
    monitor_agent.stop()
    await monitor_task
    
    logger.info("System shutdown complete.")

if __name__ == "__main__":
    asyncio.run(main())
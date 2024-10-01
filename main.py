# main.py

import asyncio
import logging
import uuid
from agents.agent_monitor import MonitorAgent
from agents.output_manager import OutputManager
from agents.agent_prompt_manager import PromptManager

async def get_user_input():
    loop = asyncio.get_event_loop()
    task_description = await loop.run_in_executor(None, lambda: input("Enter task description:\n"))
    llm_type = (await loop.run_in_executor(None, lambda: input("Select LLM to use (openai/anthropic/huggingface):\n"))).lower()
    while llm_type not in ['openai', 'anthropic', 'huggingface']:
        llm_type = (await loop.run_in_executor(None, lambda: input("Invalid LLM type. Please select openai, anthropic, or huggingface:\n"))).lower()
    return {
        'type': 'new_task',
        'id': f'task_{uuid.uuid4()}',
        'description': task_description,
        'llm_type': llm_type
    }

async def main():
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger("Main")

    logger.info("Starting the Multi-Agent System")

    output_manager = OutputManager()
    prompt_manager = PromptManager(output_manager.output_queue)
    monitor_agent = MonitorAgent(output_manager, prompt_manager)
    monitor_task = asyncio.create_task(monitor_agent.run())

    try:
        while True:
            task = await get_user_input()
            await monitor_agent.input_queue.put(task)
            logger.info(f"Submitted task {task['id']} to the system using {task['llm_type']} LLM")
            await output_manager.log_system_event(f"New task submitted: {task['id']}")

            while task['id'] not in monitor_agent.completed_tasks:
                await asyncio.sleep(1)

            logger.info(f"Task {task['id']} completed")

            quit_input = await asyncio.get_event_loop().run_in_executor(None, lambda: input("Enter 'q' to quit or any other key to submit another task:\n"))
            if quit_input.lower() == 'q':
                break
    except KeyboardInterrupt:
        logger.info("Received keyboard interrupt. Shutting down...")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
    finally:
        await monitor_agent.stop()
        await monitor_task

        output_file = await output_manager.save_to_file()
        logger.info(f"Output saved to {output_file}")

        logger.info("System shutdown complete.")

if __name__ == "__main__":
    asyncio.run(main())

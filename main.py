# main.py

import time
from agents.task_queue import task_queue
from agents.agent_project_manager import ProjectManagerAgent
from agents.agent_developer import DeveloperAgent
from agents.agent_qa import QAAgent
from agents.agent_tester import TesterAgent
from agents.agent_devops import DevOpsAgent

def process_task(user_input, model_type):
    # Step 1: Project Manager assigns a new task
    pm_agent = ProjectManagerAgent(model_type)
    task_info = pm_agent.assign_task(user_input)
    task_id = task_info['task_id']
    print(f"Task assigned: {task_id}")

    # Step 2: Developer works on the assigned task
    dev_agent = DeveloperAgent(model_type)
    dev_result = dev_agent.work_on_task(task_id)
    print(dev_result)

    # Step 3: QA Agent reviews the developed code
    qa_agent = QAAgent(model_type)
    qa_result = qa_agent.review_task(task_id)
    print(qa_result)

    # Step 4: Tester Agent tests the code
    tester_agent = TesterAgent(model_type)
    test_result = tester_agent.test_task(task_id)
    print(test_result)

    # Step 5: DevOps Agent deploys the code
    devops_agent = DevOpsAgent()
    deploy_result = devops_agent.deploy_task(task_id)
    print(deploy_result)

    return f"Task {task_id} processing complete."

def main():
    print("Welcome to the Multi-Agent Platform")

    # Get user input for task description and LLM choice
    user_input = input("Please enter your task description: ")
    print("\nSelect the LLM to use:")
    print("1. OpenAI GPT")
    print("2. Anthropic Claude")
    print("3. Hugging Face Model")
    model_choice = input("Enter the number of your choice: ")

    # Map user input to model type
    model_type = {
        '1': 'openai',
        '2': 'anthropic',
        '3': 'huggingface'
    }.get(model_choice, 'openai')  # Default to 'openai' if invalid input

    # Start worker threads
    task_queue.start_workers(3)

    # Add the task to the queue with user input and model_type
    task_queue.add_task(process_task, user_input, model_type)

    # Wait for the task to complete
    task_queue.wait_completion()

    # Retrieve and print results
    print("\nTask Results:")
    while not task_queue.result_queue.empty():
        result = task_queue.get_result()
        print(result)

    # Stop worker threads
    task_queue.stop_workers()

    print("All tasks have been processed.")

if __name__ == "__main__":
    main()

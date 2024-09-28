# agents/agent_developer.py

import os
import json
import sys
import threading

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.model_loader import llm_model

class DeveloperAgent:
    def __init__(self):
        self.tasks_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tasks')
        self.lock = threading.Lock()

    def generate_code(self, task_description):
        prompt = f"Write a Python function to {task_description}.\n\nCode:\n"
        code_snippet = llm_model.generate(prompt)
        return code_snippet

    def work_on_task(self, task_id):
        task_file = os.path.join(self.tasks_dir, f"{task_id}_task.json")
        with self.lock:
            if not os.path.exists(task_file):
                return f"Developer: Task {task_id} not found."

            with open(task_file, 'r') as f:
                task = json.load(f)
            if task['status'] != 'assigned':
                return f"Developer: Task {task_id} status is '{task['status']}'. Skipping."

            print(f"Developer is working on Task ID: {task_id}")
            code = self.generate_code(task['description'])

            # Save the generated code
            code_file = os.path.join(self.tasks_dir, f"{task_id}_code.py")
            with open(code_file, 'w') as f:
                f.write(code)

            # Update task status
            task['status'] = 'developed'
            with open(task_file, 'w') as f:
                json.dump(task, f, indent=2)

        return f"Developer: Task {task_id} completed."

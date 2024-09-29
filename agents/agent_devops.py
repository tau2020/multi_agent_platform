# agents/agent_devops.py

import os
import json
import sys
import threading
import shutil

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class DevOpsAgent:
    def __init__(self):
        self.tasks_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tasks')
        self.lock = threading.Lock()

    def deploy_task(self, task_id):
        task_file = os.path.join(self.tasks_dir, f"{task_id}_task.json")
        with self.lock:
            if not os.path.exists(task_file):
                return f"DevOps: Task {task_id} not found."

            with open(task_file, 'r') as f:
                task = json.load(f)
            if task['status'] != 'tested':
                return f"DevOps: Task {task_id} status is '{task['status']}'. Skipping."

            programming_language = task['original_input'].get('programming_language', 'Python')
            extension = 'py' if programming_language.lower() == 'python' else 'txt'
            code_file = os.path.join(self.tasks_dir, f"{task_id}_code.{extension}")
            if not os.path.exists(code_file):
                return f"DevOps: Code file for Task {task_id} not found."

            print(f"DevOps is deploying Task ID: {task_id}")
            # Simulate deployment by copying the code to a 'deployed' directory
            deployed_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'deployed')
            os.makedirs(deployed_dir, exist_ok=True)
            deployed_file = os.path.join(deployed_dir, f"{task_id}_code.{extension}")
            shutil.copyfile(code_file, deployed_file)

            # Update task status
            task['status'] = 'deployed'
            with open(task_file, 'w') as f:
                json.dump(task, f, indent=2)

        return f"DevOps: Task {task_id} deployed."

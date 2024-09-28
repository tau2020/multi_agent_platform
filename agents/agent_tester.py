# agents/agent_tester.py

import os
import json
import sys
import threading

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.model_loader import llm_model

class TesterAgent:
    def __init__(self):
        self.tasks_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tasks')
        self.lock = threading.Lock()

    def generate_tests(self, code_content):
        prompt = f"Write unit tests for the following Python code:\n\n{code_content}\n\nUnit Tests:"
        tests = llm_model.generate(prompt)
        return tests

    def test_task(self, task_id):
        task_file = os.path.join(self.tasks_dir, f"{task_id}_task.json")
        code_file = os.path.join(self.tasks_dir, f"{task_id}_code.py")
        with self.lock:
            if not os.path.exists(task_file) or not os.path.exists(code_file):
                return f"Tester: Task {task_id} not found or code not available."

            with open(task_file, 'r') as f:
                task = json.load(f)
            if task['status'] != 'reviewed':
                return f"Tester: Task {task_id} status is '{task['status']}'. Skipping."

            print(f"Tester is testing Task ID: {task_id}")
            with open(code_file, 'r') as f:
                code_content = f.read()

            tests = self.generate_tests(code_content)

            # Save the tests
            test_file = os.path.join(self.tasks_dir, f"{task_id}_test.py")
            with open(test_file, 'w') as f:
                f.write(tests)

            # Update task status
            task['status'] = 'tested'
            with open(task_file, 'w') as f:
                json.dump(task, f, indent=2)

        return f"Tester: Task {task_id} tested."

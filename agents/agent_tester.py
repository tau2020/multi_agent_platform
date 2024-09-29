# agents/agent_tester.py

import os
import json
import sys
import threading

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.model_loader import get_llm
from dotenv import load_dotenv

load_dotenv()

class TesterAgent:
    def __init__(self, model_type):
        self.tasks_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tasks')
        self.lock = threading.Lock()
        self.model_type = model_type
        self.llm_model = self.load_model()

    def load_model(self):
        # Load configuration
        config = {
            'OPENAI_API_KEY': os.getenv('OPENAI_API_KEY'),
            'ANTHROPIC_API_KEY': os.getenv('ANTHROPIC_API_KEY'),
            'HUGGINGFACE_MODEL_NAME': os.getenv('HUGGINGFACE_MODEL_NAME'),
        }
        return get_llm(self.model_type, config)

    def generate_tests(self, code_content, programming_language):
        prompt = (
            f"Write unit tests for the following {programming_language} code using an appropriate testing framework.\n\n"
            f"Code:\n{code_content}\n\n"
            "Ensure that the tests are comprehensive and do not include any print statements except those required by the testing framework."
        )
        tests = self.llm_model.generate(prompt)
        return tests

    def test_task(self, task_id):
        task_file = os.path.join(self.tasks_dir, f"{task_id}_task.json")
        programming_language = 'Python'  # Default programming language
        with self.lock:
            if not os.path.exists(task_file):
                return f"Tester: Task {task_id} not found."

            with open(task_file, 'r') as f:
                task = json.load(f)
            if task['status'] != 'reviewed':
                return f"Tester: Task {task_id} status is '{task['status']}'. Skipping."

            programming_language = task['original_input'].get('programming_language', 'Python')
            extension = 'py' if programming_language.lower() == 'python' else 'txt'
            code_file = os.path.join(self.tasks_dir, f"{task_id}_code.{extension}")
            if not os.path.exists(code_file):
                return f"Tester: Code file for Task {task_id} not found."

            print(f"Tester is testing Task ID: {task_id}")
            with open(code_file, 'r') as f:
                code_content = f.read()

            tests = self.generate_tests(code_content, programming_language)

            # Save the tests
            test_file = os.path.join(self.tasks_dir, f"{task_id}_test.{extension}")
            with open(test_file, 'w') as f:
                f.write(tests)

            # Update task status
            task['status'] = 'tested'
            with open(task_file, 'w') as f:
                json.dump(task, f, indent=2)

        return f"Tester: Task {task_id} tested."

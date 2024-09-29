# agents/agent_developer.py

import os
import json
import sys
import threading

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.model_loader import get_llm
from dotenv import load_dotenv

load_dotenv()

class DeveloperAgent:
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

    def generate_code(self, task_description, programming_language):
        prompt = (
            f"Write clean, well-documented {programming_language} code to accomplish the following task:\n\n"
            f"{task_description}\n\n"
            "Ensure that the code contains necessary comments explaining key parts, "
            "but do not include any print statements or console outputs that are not part of the core functionality."
        )
        code_snippet = self.llm_model.generate(prompt)
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
            programming_language = task['original_input'].get('programming_language', 'Python')
            code = self.generate_code(task['description'], programming_language)

            # Save the generated code
            extension = 'py' if programming_language.lower() == 'python' else 'txt'
            code_file = os.path.join(self.tasks_dir, f"{task_id}_code.{extension}")
            with open(code_file, 'w') as f:
                f.write(code)

            # Update task status
            task['status'] = 'developed'
            with open(task_file, 'w') as f:
                json.dump(task, f, indent=2)

        return f"Developer: Task {task_id} completed."

# agents/agent_qa.py

import os
import json
import sys
import threading

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.model_loader import get_llm
from dotenv import load_dotenv

load_dotenv()

class QAAgent:
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

    def review_code(self, code_content):
        prompt = f"Review the following Python code for any issues and provide suggestions:\n\n{code_content}\n\nReview:"
        review = self.llm_model.generate(prompt)
        return review

    def review_task(self, task_id):
        task_file = os.path.join(self.tasks_dir, f"{task_id}_task.json")
        code_file = os.path.join(self.tasks_dir, f"{task_id}_code.py")
        with self.lock:
            if not os.path.exists(task_file) or not os.path.exists(code_file):
                return f"QA: Task {task_id} not found or code not developed."

            with open(task_file, 'r') as f:
                task = json.load(f)
            if task['status'] != 'developed':
                return f"QA: Task {task_id} status is '{task['status']}'. Skipping."

            print(f"QA is reviewing Task ID: {task_id}")
            with open(code_file, 'r') as f:
                code_content = f.read()

            review = self.review_code(code_content)

            # Save the review
            review_file = os.path.join(self.tasks_dir, f"{task_id}_review.txt")
            with open(review_file, 'w') as f:
                f.write(review)

            # Update task status
            task['status'] = 'reviewed'
            with open(task_file, 'w') as f:
                json.dump(task, f, indent=2)

        return f"QA: Task {task_id} reviewed."

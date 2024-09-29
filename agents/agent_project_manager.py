# agents/agent_project_manager.py

import os
import json
from datetime import datetime
import sys
import threading
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.model_loader import get_llm
from dotenv import load_dotenv

load_dotenv()

class ProjectManagerAgent:
    def __init__(self, model_type):
        self.tasks_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tasks')
        os.makedirs(self.tasks_dir, exist_ok=True)
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

    def refine_task_description(self, user_input):
        prompt = f"Refine the following programming task description: {user_input}\n\nRefined task:"
        refined_description = self.llm_model.generate(prompt)
        return refined_description.split("Refined task:")[-1].strip()

    def assign_task(self, user_input):
        refined_task_description = self.refine_task_description(user_input)

        task = {
            'id': datetime.now().strftime('%Y%m%d%H%M%S%f'),
            'description': refined_task_description,
            'status': 'assigned',
            'original_input': user_input
        }

        task_file_path = os.path.join(self.tasks_dir, f"{task['id']}_task.json")
        with self.lock:
            with open(task_file_path, 'w') as f:
                json.dump(task, f, indent=2)

        return {
            'task_id': task['id'],
            'original_input': user_input,
            'refined_description': refined_task_description,
            'task_file_path': task_file_path
        }

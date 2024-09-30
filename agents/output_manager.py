import json
from datetime import datetime

class OutputManager:
    def __init__(self):
        self.output = {
            "timestamp": datetime.now().isoformat(),
            "system_log": [],
            "tasks": {},
            "final_result": None
        }

    def log_system_event(self, event):
        self.output["system_log"].append({
            "timestamp": datetime.now().isoformat(),
            "event": event
        })

    def log_task_event(self, task_id, event_type, details):
        if task_id not in self.output["tasks"]:
            self.output["tasks"][task_id] = []
        
        self.output["tasks"][task_id].append({
            "timestamp": datetime.now().isoformat(),
            "event_type": event_type,
            "details": details
        })

    def set_final_result(self, result):
        self.output["final_result"] = result

    def get_json(self):
        return json.dumps(self.output, indent=2)

    def save_to_file(self, filename):
        with open(filename, 'w') as f:
            json.dump(self.output, f, indent=2)
# agents/output_manager.py

import json
import os
from datetime import datetime
import aiofiles
import asyncio
import logging
from typing import Any, Dict

class OutputManager:
    def __init__(self, results_dir: str = None):
        self.output = {
            "timestamp": datetime.now().isoformat(),
            "system_log": [],
            "tasks": {},
            "final_product": None
        }
        self.results_dir = results_dir or os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'results')
        os.makedirs(self.results_dir, exist_ok=True)
        self.logger = logging.getLogger(self.__class__.__name__)
        self.output_queue = asyncio.Queue()  # Added output_queue

    async def log_system_event(self, event: str):
        self.output["system_log"].append({
            "timestamp": datetime.now().isoformat(),
            "event": event
        })
        self.logger.debug(f"System event logged: {event}")

    async def log_task_event(self, task_id: str, event_type: str, details: Any):
        if task_id not in self.output["tasks"]:
            self.output["tasks"][task_id] = []
        
        self.output["tasks"][task_id].append({
            "timestamp": datetime.now().isoformat(),
            "event_type": event_type,
            "details": details
        })
        self.logger.debug(f"Task event logged for {task_id}: {event_type}")

    async def set_final_product(self, final_product: Dict[str, Any]):
        self.output["final_product"] = final_product
        self.logger.debug("Final product set.")

    async def save_to_file(self) -> str:
        filename = f"output_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = os.path.join(self.results_dir, filename)
        try:
            async with aiofiles.open(filepath, 'w') as f:
                await f.write(json.dumps(self.output, indent=2))
            self.logger.info(f"Output saved to {filepath}")
            return filepath
        except Exception as e:
            self.logger.error(f"Failed to save output to file: {e}")
            raise

import asyncio
from typing import Dict
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np
import matplotlib
matplotlib.use('TkAgg')  # or another interactive backend like 'Qt5Agg'
import matplotlib.pyplot as plt

class VisualizationAgent:
    def __init__(self):
        self.fig, self.ax = plt.subplots(figsize=(12, 6))
        self.task_statuses: Dict[str, str] = {}
        self.status_colors = {
            "pending": "lightgray",
            "in_progress": "yellow",
            "completed": "green"
        }

    async def initialize(self):
        plt.ion()  # Turn on interactive mode
        self.ax.set_title("Task Completion Status")
        self.ax.set_xlabel("Tasks")
        self.ax.set_ylabel("Status")
        plt.tight_layout()
        plt.show(block=False)

    async def update_task_status(self, task_id: str, status: str):
        self.task_statuses[task_id] = status
        await self.redraw()

    async def redraw(self):
        self.ax.clear()
        tasks = list(self.task_statuses.keys())
        colors = [self.status_colors[status] for status in self.task_statuses.values()]
        
        y_pos = np.arange(len(tasks))
        self.ax.barh(y_pos, [1] * len(tasks), align='center', color=colors)
        self.ax.set_yticks(y_pos)
        self.ax.set_yticklabels(tasks)
        self.ax.invert_yaxis()
        
        self.ax.set_title("Task Completion Status")
        self.ax.set_xlabel("Status")
        
        plt.tight_layout()
        plt.draw()
        plt.pause(0.001)

    async def show_completion_message(self, message: str):
        self.ax.text(0.5, -0.1, message, ha='center', va='center', transform=self.ax.transAxes, fontsize=12, color='blue')
        plt.draw()
        plt.pause(0.001)

    async def show_product_location(self, file_path: str):
        self.ax.text(0.5, -0.2, f"Final product saved at: {file_path}", ha='center', va='center', transform=self.ax.transAxes, fontsize=10, color='green')
        plt.draw()
        plt.pause(0.001)

    async def shutdown(self):
        plt.close(self.fig)

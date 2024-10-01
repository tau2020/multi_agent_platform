import asyncio
from datetime import datetime
import logging
import json
import uuid
import re
import sys
from typing import Any, Dict
from agents.agent_developer import DeveloperAgent
from agents.agent_visualization import VisualizationAgent
from agents.model_loader import get_llm
from agents.agent_prompt_manager import PromptManager
from agents.llm_response_resolver import LLMResponseResolver

class MonitorAgent:
    def __init__(self, output_manager: Any, prompt_manager: PromptManager, num_workers: int = 5):
        self.input_queue = asyncio.Queue()
        self.output_queue = asyncio.Queue()
        self.agents: Dict[str, DeveloperAgent] = {}
        self.completed_tasks = set()
        self.task_results: Dict[str, Any] = {}
        self.logger = logging.getLogger('MonitorAgent')
        self.llm = None
        self.output_manager = output_manager
        self.prompt_manager = prompt_manager
        self.num_workers = num_workers
        self.workers = []
        self.final_product = {}
        self.visualization_agent = VisualizationAgent()
        self.agent_scores = {}
        self.task_start_times = {}
        self.total_tasks = 0
        self.completed_tasks = set()
        self.task_results: Dict[str, Any] = {}

        self.llm_resolver = LLMResponseResolver()

    async def run(self):
        self.logger.info("Monitor Agent started.")
        await self.output_manager.log_system_event("Monitor Agent started.")
        await self.visualization_agent.initialize()
        workers = [asyncio.create_task(self.worker()) for _ in range(self.num_workers)]
        self.workers.extend(workers)
        try:
            await asyncio.gather(*workers)
        except Exception as e:
            await self.handle_critical_error(f"Error in Monitor Agent: {str(e)}")
        finally:
            await self.finalize_process()
            
            
    async def worker(self):
        while True:
            try:
                message = await asyncio.wait_for(self.input_queue.get(), timeout=1)
                if message.get('type') == 'terminate':
                    self.logger.info("Monitor Agent terminating worker.")
                    break
                if message.get('type') == 'new_task':
                    await self.process_task(message)
                elif message.get('type') == 'task_completed':
                    await self.handle_completed_task(message)
            except asyncio.TimeoutError:
                continue
            except Exception as e:
                await self.handle_critical_error(f"Error in worker: {str(e)}")

    async def process_task(self, task: Dict[str, Any]):
        self.llm = get_llm(task['llm_type'], {})
        try:
            subtasks = await self.breakdown_task(task)
            self.total_tasks += len(subtasks)
            for subtask in subtasks:
                await self.prompt_manager.assign_role_and_delegate(subtask, self.output_queue, self.llm)
        except Exception as e:
            await self.handle_critical_error(f"Error processing task: {str(e)}")

    async def breakdown_task(self, task: Dict[str, Any]):
        prompt = f"""
        Analyze the following task and break it down into subtasks:
        Task: {task['description']}
        
        Provide the subtasks in valid JSON format with the following structure:
        {{
            "subtasks": [
                {{
                    "task": "Subtask name",
                    "description": "Subtask description",
                    "complexity": 1-5 (optional)
                }},
                ...
            ]
        }}
        """
        raw_result = await asyncio.get_event_loop().run_in_executor(None, self.llm.generate, prompt)
        
        resolved_result = self.llm_resolver.resolve(task['llm_type'], raw_result)
        self.logger.debug(f"Resolved LLM response: {resolved_result}")
        await self.output_manager.log_task_event(task['id'], "llm_response", resolved_result)
        
        try:
            result_content = resolved_result['content']
            self.logger.debug(f"Raw LLM content: {result_content}")
            
            if not result_content.strip():
                raise ValueError("LLM returned an empty response")
            
            # Remove code fence if present
            json_str = re.sub(r'^```json\s*|\s*```$', '', result_content, flags=re.MULTILINE).strip()
            
            self.logger.debug(f"Extracted JSON string: {json_str}")
            
            subtasks_data = json.loads(json_str)
            
            if not isinstance(subtasks_data, dict) or 'subtasks' not in subtasks_data:
                raise ValueError("Invalid JSON structure: expected a 'subtasks' key")
            
            subtasks = subtasks_data['subtasks']
            if not isinstance(subtasks, list):
                raise ValueError("Expected 'subtasks' to be a list")
            
            valid_subtasks = []
            for i, subtask in enumerate(subtasks):
                if not all(k in subtask for k in ('task', 'description')):
                    self.logger.warning(f"Skipping invalid subtask: {subtask}")
                    continue
                
                # Assign an ID to the subtask
                subtask_id = f"{task['id']}_subtask_{i+1}"
                valid_subtask = {
                    'id': subtask_id,
                    'description': f"{subtask['task']}: {subtask['description']}",
                    'complexity': subtask.get('complexity', 1)
                }
                
                if not isinstance(valid_subtask['complexity'], int) or not 1 <= valid_subtask['complexity'] <= 5:
                    self.logger.warning(f"Invalid complexity in subtask, setting to 1: {subtask}")
                    valid_subtask['complexity'] = 1
                
                valid_subtasks.append(valid_subtask)
            
            if not valid_subtasks:
                raise ValueError("No valid subtasks found")
            
            self.total_tasks += len(valid_subtasks)
            await self.output_manager.log_task_event(task['id'], "subtasks", valid_subtasks)
            return valid_subtasks

        except json.JSONDecodeError as e:
            error_msg = f"Failed to parse LLM response as JSON: {str(e)}\nRaw content: {result_content}"
            self.logger.error(error_msg)
            await self.output_manager.log_task_event(task['id'], "error", error_msg)
            raise ValueError(error_msg)
        except ValueError as e:
            error_msg = f"Invalid subtask format: {str(e)}\nRaw content: {result_content}"
            self.logger.error(error_msg)
            await self.output_manager.log_task_event(task['id'], "error", error_msg)
            raise ValueError(error_msg)

    async def handle_completed_task(self, message: Dict[str, Any]):
        task_id = message['task_id']
        self.completed_tasks.add(task_id)
        self.task_results[task_id] = message.get('result', "No result provided")
        self.logger.info(f"Task {task_id} completed by {message['agent_id']}")
        await self.output_manager.log_task_event(task_id, "completed", {
            "agent_id": message['agent_id'],
            "result": self.task_results[task_id]
        })
        await self.visualization_agent.update_task_status(task_id, "completed")
        
        if self.all_tasks_complete():
            await self.finalize_process()

            
    def all_tasks_complete(self):
        return len(self.completed_tasks) == self.total_tasks and self.total_tasks > 0
       
            
    def calculate_agent_score(self, completion_time: float, quality: float, complexity: int) -> float:
        time_score = max(0, 100 - completion_time)  # Assumes 100 seconds is the target time
        return (time_score * 0.4 + quality * 100 * 0.4 + complexity * 20 * 0.2) / 100


    async def announce_task_completion(self, task_id: str, agent_id: str, score: float):
        announcement = f"Task {task_id} completed by {agent_id} with a score of {score:.2f}!"
        self.logger.info(announcement)
        await self.output_manager.log_system_event(announcement)


    async def announce_all_tasks_completed(self):
        announcement = "All tasks have been completed! Generating final product..."
        self.logger.info(announcement)
        await self.output_manager.log_system_event(announcement)
        await self.visualization_agent.show_completion_message(announcement)
     
    async def finalize_process(self):
        if not self.all_tasks_complete():
            return
        
        self.logger.info("All tasks completed. Finalizing process.")
        await self.output_manager.log_system_event("All tasks completed. Finalizing process.")
        await self.integrate_results()
        await self.output_final_product()
        await self.stop()


    async def integrate_results(self):
        self.logger.info("Integrating results from all completed tasks.")
        integrated_result = {}
        for task_id, result in self.task_results.items():
            integrated_result[task_id] = result
        
        self.final_product = {
            "integrated_result": integrated_result,
            "summary": await self.generate_summary()
        }
        
        self.logger.info("Results integrated successfully.")
        await self.output_manager.log_system_event("Results integrated successfully.")

    async def generate_summary(self):
        prompt = f"""
        Summarize the following task results into a cohesive final product:
        {json.dumps(self.task_results, indent=2)}
    
        Provide a brief summary of the overall task, the approach taken, and the key outcomes.
        """
        raw_summary = await asyncio.get_event_loop().run_in_executor(None, self.llm.generate, prompt)
        
        resolved_summary = self.llm_resolver.resolve(self.llm.type, raw_summary)
        return resolved_summary['content']

    async def output_final_product(self):
        output_file = 'final_product.json'
        try:
            with open(output_file, 'w') as f:
                json.dump(self.final_product, f, indent=2)
            self.logger.info(f"Final product saved to {output_file}")
            await self.output_manager.log_system_event(f"Final product saved to {output_file}")
            await self.visualization_agent.show_product_location(output_file)
        except Exception as e:
            await self.handle_critical_error(f"Error saving final product: {str(e)}")

    async def stop(self):
        for agent in self.agents.values():
            await agent.input_queue.put({'type': 'terminate'})
        await self.output_manager.log_system_event("Monitor Agent stopped.")
        await self.output_manager.save_to_file()
        for worker in self.workers:
            worker.cancel()
        await self.visualization_agent.shutdown()


    async def handle_critical_error(self, error_message: str):
        self.logger.critical(error_message)
        await self.output_manager.log_system_event(f"CRITICAL ERROR: {error_message}")
        await self.stop()
        sys.exit(1)
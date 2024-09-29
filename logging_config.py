# logging_config.py

import logging

def setup_logging():
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
        handlers=[
            logging.FileHandler('multi_agent_system.log'),
            logging.StreamHandler()
        ]
    )

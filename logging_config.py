# Imports libraries
import logging


def setup_logging():
    # Set up the basic logging configuration
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(
                "logs/debug.log"),  # Log to a file
            logging.StreamHandler()  # Log to the console
        ]
    )

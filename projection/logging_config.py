### /Users/robinsongarcia/projects/gnomonic/projection/logging_config.py ###

"""
Logging configuration for the Gnomonic Projection module.
"""

import logging
import sys

def setup_logging():
    """
    Set up logging configuration.
    """
    logger = logging.getLogger('gnomonic_projection')
    logger.setLevel(logging.DEBUG)  # Set to DEBUG to capture all levels of logs

    # Create handlers
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)  # Set to INFO for console output

    file_handler = logging.FileHandler('gnomonic_projection.log')
    file_handler.setLevel(logging.DEBUG)  # Detailed logs in file

    # Create formatters and add them to handlers
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # Add handlers to the logger
    if not logger.hasHandlers():
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    return logger
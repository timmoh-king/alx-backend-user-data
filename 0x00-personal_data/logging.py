#!/usr/bin/env python3

import logging

logging.basicConfig(
    level=logging.DEBUG,  # Set the minimum logging level to capture
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),  # Output to the console
        logging.FileHandler('app.log')  # Output to a file
    ]
)

logging.debug("This is a debug message.")
logging.info("This is an info message.")
logging.warning("This is a warning message.")
logging.error("This is an error message.")
logging.critical("This is a critical message.")

logger = logging.getLogger("my_logger")
logger.warning("This is a warning from my_logger.")

name = "John"
age = 30
logging.info("User: %s, Age: %d", name, age)

try:
    result = 10 / 0
except Exception as e:
    logging.error("An error occurred: %s", str(e), exc_info=True)

# Using a configuration file
logging.config.fileConfig('logging.conf')

# Programmatically configuring a logger
logger = logging.getLogger("my_logger")
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

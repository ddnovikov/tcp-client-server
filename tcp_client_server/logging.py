import logging
import sys

LOG_CONF = {'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            'datefmt': '%m/%d/%Y %I:%M:%S %p',
            'stream': sys.stdout,
            'level': logging.DEBUG}

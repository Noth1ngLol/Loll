import os
import logging
import sys

class Logger:
    def __init__(self):
        self.logger = logging.getLogger('GGUF Manager')
        self.logger.setLevel(logging.INFO)
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.verbose = False

    def set_verbose(self, verbose):
        self.verbose = verbose
        if verbose:
            self.logger.setLevel(logging.DEBUG)
        else:
            self.logger.setLevel(logging.INFO)

    def debug(self, message):
        if self.verbose:
            self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

logger = Logger()

def validate_file_path(file_path):
    if not os.path.exists(file_path):
        logger.error(f"File not found: {file_path}")
        sys.exit(1)
    if not os.path.isfile(file_path):
        logger.error(f"Not a file: {file_path}")
        sys.exit(1)
    return os.path.abspath(file_path)

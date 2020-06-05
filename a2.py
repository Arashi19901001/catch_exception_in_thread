import time
from setup_logger import setup_logger


class A2:
    def __init__(self):
        self.logger = setup_logger("a2")

    def run(self):
        for i in range(10):
            self.logger.info("a2: {}".format(i))
            time.sleep(1)

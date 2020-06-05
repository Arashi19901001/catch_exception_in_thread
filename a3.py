import time
from setup_logger import setup_logger


class A3:
    def __init__(self):
        self.logger = setup_logger("a3")

    def run(self):
        for i in range(10):
            self.logger.info("a3: {}".format(i))
            time.sleep(1)
        raise Exception("error")

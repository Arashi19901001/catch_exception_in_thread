import threading
import sys
import time
from setup_logger import setup_logger
from a1 import A1
from a2 import A2
from a3 import A3


def patch_threading_excepthook():
    """Installs our exception handler into the threading modules Thread object
    Inspired by https://bugs.python.org/issue1230540
    """
    old_init = threading.Thread.__init__

    def new_init(self, *args, **kwargs):
        old_init(self, *args, **kwargs)
        old_run = self.run

        def run_with_our_excepthook(*args, **kwargs):
            try:
                old_run(*args, **kwargs)
            except (KeyboardInterrupt, SystemExit):
                raise
            except Exception:
                sys.excepthook(*sys.exc_info())
        self.run = run_with_our_excepthook
    threading.Thread.__init__ = new_init


patch_threading_excepthook()


class Main:
    def __init__(self):
        self.logger = setup_logger("main")
        self.a1 = A1()
        self.a2 = A2()
        self.a3 = A3()
        self.threads = list()
        sys.excepthook = self.handle_exception

    def handle_exception(self, exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt) or issubclass(exc_type, SystemExit):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return

        self.logger.critical("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))

    def main_run(self):
        for i in range(10):
            self.logger.info("main: {}".format(i))
            time.sleep(1)
        1 / 0

    def run(self):
        self.logger.info("begin")
        t = threading.Thread(target=self.a1.run)
        self.threads.append(t)
        t = threading.Thread(target=self.a2.run)
        self.threads.append(t)
        t = threading.Thread(target=self.a3.run)
        self.threads.append(t)
        t = threading.Thread(target=self.main_run)
        self.threads.append(t)

        for t in self.threads:
            t.start()
        for t in self.threads:
            t.join()
        self.logger.info("stop")


if __name__ == "__main__":
    m = Main()
    m.run()

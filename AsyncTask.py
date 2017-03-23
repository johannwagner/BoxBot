from threading import Thread

import time


class AsyncTask(Thread):
    task = None
    timeout = 60
    running = True

    def __init__(self, timeout, group=None, target=None, name=None, args=(), kwargs=None, *, daemon=None):
        super().__init__(group, target, name, args, kwargs, daemon=daemon)
        self.timeout = timeout

    def run(self):
        super().run()

        while self.running:
            if self.task is not None:
                self.task()

            time.sleep(self.timeout)

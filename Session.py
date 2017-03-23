import datetime

import pickle
import threading


class Session:


    loaded = False
    lock = threading.Lock()
    logger = None
    channels = []
    closed_issues = []
    open_issues = []
    last_request_time = None

    def __init__(self, logger):
        self.logger = logger

    def load(self):
        self.lock.acquire()
        try:
            self.channels = pickle.load(open("channels.p", "rb"))
            self.closed_issues = pickle.load(open("closed_bugs.p", "rb"))
            self.open_issues = pickle.load(open("open_issues.p", "rb"))
            self.last_request_time =  pickle.load(open("last_request_time.p", "rb"))
            print("Session loaded.")
        except:
            print("Session could not be loaded.")
        finally:
            self.lock.release()
            self.loaded = True

            if self.last_request_time is None:
                self.last_request_time = datetime.datetime.now(datetime.timezone.utc)

    def save(self):
        self.lock.acquire()
        try:
            pickle.dump(self.channels, open("channels.p", "wb"))
            pickle.dump(self.closed_issues, open("closed_bugs.p", "wb"))
            pickle.dump(self.open_issues, open("open_issues.p", "wb"))
            pickle.dump(self.last_request_time, open("last_request_time.p", "wb"))
            print("Session saved.")
        except:
            print("Session could not be saved.")
        finally:
            self.lock.release()
import datetime
import os

import pickle
import threading
from logging import Logger

import discord

from ChatManager import ChatManager
from UserManager import UserManager


class Session:
    client = None
    user_manager = None
    chat_manager = None
    logger = None

    loaded = False
    lock = threading.Lock()

    closed_issues = []
    open_issues = []
    comments = []
    user_manager_data = {}
    chat_manager_data = {}

    last_request_time = None

    def __init__(self, client: discord.Client, logger: Logger):
        self.client = client
        self.logger = logger

    def load(self):
        self.lock.acquire()
        try:
            self.closed_issues = pickle.load(open("data/closed_bugs.p", "rb"))
            self.open_issues = pickle.load(open("data/open_issues.p", "rb"))
            self.comments = pickle.load(open("data/comments.p", "rb"))
            self.last_request_time = pickle.load(open("data/last_request_time.p", "rb"))
            self.user_manager_data = pickle.load(open("data/user_manager_data.p", "rb"))
            self.chat_manager_data = pickle.load(open("data/chat_manager_data.p", "rb"))
            self.logger.info("Session loaded.")
        except:
            self.logger.error("Session could not be loaded.")
        finally:
            self.lock.release()
            self.loaded = True

            if self.last_request_time is None:
                self.last_request_time = datetime.datetime.now(datetime.timezone.utc)
            if self.user_manager is None:
                self.user_manager = UserManager(self.client, self)
            if self.chat_manager is None:
                self.chat_manager = ChatManager(self)

    def save(self):
        self.lock.acquire()
        directory = "data"
        if not os.path.exists(directory):
            os.makedirs(directory)
        try:
            pickle.dump(self.closed_issues, open("data/closed_bugs.p", "wb"))
            pickle.dump(self.open_issues, open("data/open_issues.p", "wb"))
            pickle.dump(self.comments, open("data/comments.p", "wb"))
            pickle.dump(self.last_request_time, open("data/last_request_time.p", "wb"))
            pickle.dump(self.user_manager_data, open("data/user_manager_data.p", "wb"))
            pickle.dump(self.chat_manager_data, open("data/chat_manager_data.p", "wb"))
            self.logger.info("Session saved.")
        except:
            self.logger.error("Session could not be saved.")
        finally:
            self.lock.release()

import logging
import logging.handlers
import uuid
import datetime
import time
import threading

import rpyc

from models import users
import torch


class Kos(rpyc.Service):
    def __init__(self, host, user, passwd):
        super().__init__()
        logging_handler = logging.handlers.RotatingFileHandler(
            'logs/Kos.log',
            'a',
            1024 * 1024,
            10,
            'utf-8'
        )
        logging_format = logging.Formatter(
            '%(asctime)s [%(name)s - %(levelname)s] %(message)s'
        )
        logging_handler.setFormatter(logging_format)
        logger = logging.getLogger()
        logger.addHandler(logging_handler)
        logger.setLevel(logging.DEBUG)

        self.login_users = dict()
        self.host = host
        self.user = user
        self.passwd = passwd
        self.session_period = 30

        thread_cleaning = threading.Thread(
            target=self.clear_session, daemon=True
        )
        thread_cleaning.start()

    def on_connect(self, conn):
        pass

    def on_disconnect(self, conn):
        pass

    def clear_session(self):
        while True:
            datetime_now = datetime.datetime.now()
            for k, v in list(self.login_users.items()):
                if v['expired'] < datetime_now:
                    del self.login_users[k]
            time.sleep(self.session_period)

    def exposed_get_environments(self):
        return ['开发环境', '测试环境', '生产环境']

    def exposed_login(self, session_id, user, passwd):
        user = users.login(self.host, self.user, self.passwd, user, passwd)
        if user and user[0]:
            token = str(uuid.uuid4())
            expired = datetime.datetime.now() +\
                datetime.timedelta(seconds=self.session_period)
            self.login_users[session_id] = {
                'id': user[0],
                'token': token,
                'expired': expired
            }
            return token
        else:
            return None

    def exposed_logout(self, session_id):
        removed = self.login_users.pop(session_id, None)
        return removed

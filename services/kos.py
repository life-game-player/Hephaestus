import logging
import logging.handlers
import uuid

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

    def on_connect(self, conn):
        logging.debug(conn)

    def on_disconnect(self, conn):
        pass

    def exposed_get_environments(self):
        return ['开发环境', '测试环境', '生产环境']

    def exposed_login(self, session_id, user, passwd):
        user = users.login(self.host, self.user, self.passwd, user, passwd)
        if user and user[0]:
            token = str(uuid.uuid4())
            self.login_users[(session_id, token)] = user[0]
            return token
        else:
            return None

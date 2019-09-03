import uuid
import datetime
import time
import threading

import rpyc

from models import users
from models import mysql
from models import environments
from models import mnemosyne
from clio import logger


class Kos(rpyc.Service):
    def __init__(self, host, user, passwd):
        super().__init__()

        self.login_users = dict()
        self.host = host
        self.user = user
        self.passwd = passwd
        self.session_period = 10  # session过期时间(秒)

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

    def exposed_get_tenants(self, session_id, token, count=None):
        if (
            session_id in self.login_users and
            token == self.login_users[session_id]['token']
        ):
            # token有效
            tenants = list()
            if count:
                for i in range(count):
                    tenants.append(
                        {'id': i, 'name': '商户{}'.format(i)}
                    )
            else:
                for i in range(30):
                    tenants.append(
                        {'id': i, 'name': '商户{}'.format(i)}
                    )
            return tenants
        else:
            # token失效
            return -1

    def exposed_create_env(
        self, session_id, token,
        env, read_host, write_host, user, passwd
    ):
        if (
            session_id in self.login_users and
            token == self.login_users[session_id]['token']
        ):
            # token有效
            operator = self.login_users[session_id]['id']
            result = 999
            if write_host and user and passwd:
                result1 = 0
                result2 = 0
                if read_host:
                    result1 = mysql.test(read_host, user, passwd)
                result2 = mysql.test(write_host, user, passwd)
                result = result1 + result2
                if not result:
                    # 插入数据库
                    if environments.create(
                        self.host,
                        self.user,
                        self.passwd,
                        env, read_host, write_host, user, passwd
                    ):
                        result = 3
            else:
                result = 2
            mnemosyne.create(
                self.host,
                self.user,
                self.passwd,
                operator, 1, 1 if result else 0
            )
        else:
            # token失效
            result = -1
        return result

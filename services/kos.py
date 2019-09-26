import uuid
import datetime
import time
import threading

import rpyc

from models import users
from models import mysql
from models import environments
from models import mnemosyne
from models import tenants
from models import permissions


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

    def exposed_get_environments(self, session_id, token):
        if (
            session_id in self.login_users and
            token == self.login_users[session_id]['token']
        ):
            # token有效
            operator = self.login_users[session_id]['id']

            # 检查用户是否为管理员
            operator_info = users.get(
                self.host, self.user, self.passwd, operator
            )
            if (
                operator_info and
                int.from_bytes(operator_info[0]['dominated'], 'big')
            ):
                return environments.list(
                    self.host, self.user, self.passwd
                )
            else:
                return environments.list(
                    self.host, self.user, self.passwd,
                    operator
                )
        else:
            # token失效
            return -1

    def exposed_login(self, session_id, user, passwd):
        login_result = users.login(
            self.host, self.user, self.passwd, user, passwd
        )
        if login_result:
            if login_result[1]:
                # 用户被禁用
                return 'DISABLED', None, None
            elif login_result[0]:
                token = str(uuid.uuid4())
                expired = datetime.datetime.now() +\
                    datetime.timedelta(seconds=self.session_period)
                self.login_users[session_id] = {
                    'id': login_result[0],
                    'token': token,
                    'expired': expired
                }
                user_info = users.get(
                    self.host, self.user, self.passwd, login_result[0]
                )
                username = None
                role = None
                if user_info:
                    username = user_info[0]['name']
                    role = '管理员' \
                        if int.from_bytes(user_info[0]['dominated'], 'big') \
                        else '普通用户'
                return token, username, role
            else:
                # 密码不正确
                return None, None, None
        else:
            # 用户不存在
            return None, None, None

    def exposed_logout(self, session_id):
        removed = self.login_users.pop(session_id, None)
        return removed

    def exposed_get_tenants(self, env, session_id, token):
        if (
            session_id in self.login_users and
            token == self.login_users[session_id]['token']
        ):  # token有效
            operator = self.login_users[session_id]['id']
            # 检查用户权限
            operator_info = users.get(
                self.host, self.user, self.passwd, operator
            )
            if (
                operator_info and
                int.from_bytes(operator_info[0]['dominated'], 'big')
            ):
                env_info = environments.get(
                    self.host, self.user, self.passwd, env
                )
            else:
                env_info = environments.get(
                    self.host, self.user, self.passwd, env,
                    operator
                )
                print(env_info, operator)
            if env_info:
                list_tenants = tenants.list(
                    env_info[0]['read_host'],
                    env_info[0]['user'],
                    env_info[0]['passwd']
                )
                return list_tenants if list_tenants else list()
            else:
                return 1  # 环境无效
        else:  # token失效
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

            # 检查用户权限
            operator_info = users.get(
                self.host, self.user, self.passwd, operator
            )
            if (
                operator_info and
                int.from_bytes(operator_info[0]['dominated'], 'big')
            ):
                result = 999
                if write_host and user and passwd:
                    result1 = 0
                    result2 = 0
                    if read_host:
                        result1 = mysql.test(read_host, user, passwd)
                    result2 = mysql.test(write_host, user, passwd)
                    result = result1 + result2
                    if not result:
                        # 是否存在重复的环境
                        dup_env = environments.find_duplicate(
                            self.host,
                            self.user,
                            self.passwd,
                            env, read_host, write_host
                        )
                        if dup_env is None:
                            result = 3  # 数据库错误
                        elif dup_env:
                            return dup_env[0]['name']
                        else:
                            # 插入数据库
                            if environments.create(
                                self.host,
                                self.user,
                                self.passwd,
                                env, read_host, write_host, user, passwd
                            ):
                                result = 3  # 数据库错误
                else:
                    result = 2  # 写库连接失败
            else:
                result = 4  # 用户权限不足
            mnemosyne.create(
                self.host,
                self.user,
                self.passwd,
                'environment',
                operator, 1, 1 if result else 0
            )
        else:
            # token失效
            result = -1
        return result

    def exposed_create_user(
        self, session_id, token,
        username, passwd, user_permission
    ):
        if (
            session_id in self.login_users and
            token == self.login_users[session_id]['token']
        ):
            # token有效
            operator = self.login_users[session_id]['id']

            # 检查用户权限
            operator_info = users.get(
                self.host, self.user, self.passwd, operator
            )
            if (
                operator_info and
                int.from_bytes(operator_info[0]['dominated'], 'big')
            ):
                result = 999
                # 是否存在重复的用户
                dup_user = users.find_duplicate(
                    self.host, self.user, self.passwd, username
                )
                if dup_user is None:
                    result = 1  # 数据库错误
                elif dup_user:
                    return dup_user[0]['name']
                else:
                    # 插入数据库
                    result = 0
                    if users.create(
                        self.host, self.user, self.passwd,
                        username, passwd, user_permission
                    ):
                        result = 1
            else:
                result = 2  # 用户权限不足
            mnemosyne.create(
                self.host,
                self.user,
                self.passwd,
                'user',
                operator, 1, 1 if result else 0
            )
        else:
            # token失效
            result = -1
        return result

    def exposed_get_users(
        self, session_id, token
    ):
        if (
            session_id in self.login_users and
            token == self.login_users[session_id]['token']
        ):
            # token有效
            operator = self.login_users[session_id]['id']

            # 检查用户权限
            operator_info = users.get(
                self.host, self.user, self.passwd, operator
            )
            if (
                operator_info and
                int.from_bytes(operator_info[0]['dominated'], 'big')
            ):
                result = users.list(
                    self.host,
                    self.user,
                    self.passwd
                )
            else:
                result = 2  # 用户权限不足
            mnemosyne.create(
                self.host,
                self.user,
                self.passwd,
                'user',
                operator, 3, 1 if result else 0
            )
        else:
            # token失效
            result = -1
        return result

    def exposed_get_user(
        self, session_id, token, user_id
    ):
        if (
            session_id in self.login_users and
            token == self.login_users[session_id]['token']
        ):
            # token有效
            operator = self.login_users[session_id]['id']

            # 检查用户权限
            operator_info = users.get(
                self.host, self.user, self.passwd, operator
            )
            if (
                operator_info and
                int.from_bytes(operator_info[0]['dominated'], 'big')
            ):
                result = users.get(
                    self.host,
                    self.user,
                    self.passwd,
                    user_id
                )
            else:
                result = 2  # 用户权限不足
            mnemosyne.create(
                self.host,
                self.user,
                self.passwd,
                'user',
                operator, 3, 1 if result else 0
            )
        else:
            # token失效
            result = -1
        return result

    def exposed_get_permission_by_user(
        self, session_id, token, user_id
    ):
        if (
            session_id in self.login_users and
            token == self.login_users[session_id]['token']
        ):
            # token有效
            operator = self.login_users[session_id]['id']

            # 检查用户权限
            operator_info = users.get(
                self.host, self.user, self.passwd, operator
            )
            if (
                operator_info and
                int.from_bytes(operator_info[0]['dominated'], 'big')
            ):
                result = permissions.get_by_user(
                    self.host,
                    self.user,
                    self.passwd,
                    user_id
                )
            else:
                result = 2  # 用户权限不足
            mnemosyne.create(
                self.host,
                self.user,
                self.passwd,
                'permission',
                operator, 3, 1 if result else 0
            )
        else:
            # token失效
            result = -1
        return result

    def exposed_update_permission_by_user(
        self, session_id, token, user_permisson, user_id
    ):
        if (
            session_id in self.login_users and
            token == self.login_users[session_id]['token']
        ):
            # token有效
            operator = self.login_users[session_id]['id']

            # 检查用户权限
            operator_info = users.get(
                self.host, self.user, self.passwd, operator
            )
            if (
                operator_info and
                int.from_bytes(operator_info[0]['dominated'], 'big')
            ):
                result = permissions.update_by_user(
                    self.host,
                    self.user,
                    self.passwd,
                    user_permisson,
                    user_id
                )
            else:
                result = 2  # 用户权限不足
            mnemosyne.create(
                self.host,
                self.user,
                self.passwd,
                'permission',
                operator, 2, 1 if result else 0
            )
        else:
            # token失效
            result = -1
        return result

    def exposed_update_user_status(
        self, session_id, token, user_status, user_id
    ):
        if (
            session_id in self.login_users and
            token == self.login_users[session_id]['token']
        ):
            # token有效
            operator = self.login_users[session_id]['id']

            # 检查用户权限
            operator_info = users.get(
                self.host, self.user, self.passwd, operator
            )
            if (
                operator_info and
                int.from_bytes(operator_info[0]['dominated'], 'big')
            ):
                result = users.update_user_status(
                    self.host,
                    self.user,
                    self.passwd,
                    user_status,
                    user_id
                )
                for k, v in list(self.login_users.items()):
                    if v['id'] == user_id:
                        del self.login_users[k]
            else:
                result = 2  # 用户权限不足
            mnemosyne.create(
                self.host,
                self.user,
                self.passwd,
                'user',
                operator, 2, 1 if result else 0
            )
        else:
            # token失效
            result = -1
        return result

    def exposed_delete_user(
        self, session_id, token, user_id
    ):
        if (
            session_id in self.login_users and
            token == self.login_users[session_id]['token']
        ):
            # token有效
            operator = self.login_users[session_id]['id']

            # 检查用户权限
            operator_info = users.get(
                self.host, self.user, self.passwd, operator
            )
            if (
                operator_info and
                int.from_bytes(operator_info[0]['dominated'], 'big')
            ):
                result = users.delete(
                    self.host,
                    self.user,
                    self.passwd,
                    user_id
                )
                for k, v in list(self.login_users.items()):
                    if v['id'] == user_id:
                        del self.login_users[k]
            else:
                result = 2  # 用户权限不足
            mnemosyne.create(
                self.host,
                self.user,
                self.passwd,
                'user',
                operator, 4, 1 if result else 0
            )
        else:
            # token失效
            result = -1
        return result

    def exposed_update_user_passwd(
        self, session_id, token,
        user_id, passwd
    ):
        if (
            session_id in self.login_users and
            token == self.login_users[session_id]['token']
        ):
            # token有效
            operator = self.login_users[session_id]['id']

            # 检查用户权限
            operator_info = users.get(
                self.host, self.user, self.passwd, operator
            )
            if (
                operator_info and
                int.from_bytes(operator_info[0]['dominated'], 'big')
            ):
                result = users.update_passwd(
                    self.host,
                    self.user,
                    self.passwd,
                    user_id,
                    passwd
                )
            else:
                result = 2  # 用户权限不足
            mnemosyne.create(
                self.host,
                self.user,
                self.passwd,
                'user',
                operator, 2, 1 if result else 0
            )
        else:
            # token失效
            result = -1
        return result

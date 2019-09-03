import secrets
import uuid

import torch
from clio import logger


def create(
    host, user, passwd,
    env, env_read_host, env_write_host, env_user, env_passwd
):
    result = 0
    conn = torch.connect(host, user, passwd, 'hephaestus')
    try:
        guid = str(uuid.uuid4())
        vector = secrets.token_bytes(16)
        sql = (
            "INSERT INTO islands"
            "(name, read_host, write_host, user, secret, guid, vector) "
            "VALUES(%s, %s, %s, %s, "
            "CBC_ENCRYPT(%s, %s, _binary %s), "
            "%s, _binary %s)"
        )
        torch.execute(
            conn, sql,
            (
                env, env_read_host, env_write_host, env_user,
                guid, env_passwd, vector,
                guid, vector
            )
        )
    except Exception as e:
        result = 1
        logger.error(
            "{} occured".format(type(e).__name__),
            exc_info=True
        )
    return result


def get(
    host, user, passwd,
    env, env_read_host, env_write_host
):
    conn = torch.connect(host, user, passwd, 'hephaestus')
    sql = (
        "SELECT `name` FROM islands "
        "WHERE `name` = '{}' "
        "OR read_host = '{}' "
        "OR write_host = '{}' "
    ).format(
        env, env_read_host, env_write_host
    )
    return torch.query(conn, sql)

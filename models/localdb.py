import sqlite3

from clio import logger


local_db = 'local.db'


def init_localdb():
    update_local_db(
        "CREATE TABLE IF NOT EXISTS favourite_tenants("
        "id BIGINT NOT NULL, "
        "env VARCHAR(30) NOT NULL, "
        "visit_count INT NOT NULL DEFAULT 0, "
        "visited TIMESTAMP DEFAULT CURRENT_TIMESTAMP, "
        "PRIMARY KEY(id, env)"
        ")"
    )


def connect_local_db():
    return sqlite3.connect(local_db)


def query_local_db(sql):
    results = None
    try:
        conn = connect_local_db()
        c = conn.cursor()
        c.execute(sql)
        results = c.fetchall()
    except Exception as e:
        logger.error(
            "{} occured".format(type(e).__name__),
            exc_info=True
        )
    finally:
        conn.close()
    return results


def update_local_db(sql):
    try:
        conn = connect_local_db()
        c = conn.cursor()
        c.execute(sql)
        conn.commit()
    except Exception as e:
        conn.rollback()
        logger.error(
            "{} occured".format(type(e).__name__),
            exc_info=True
        )
    finally:
        conn.close()


def visit_tenant(id, env):
    update_local_db(
        "INSERT INTO favourite_tenants(id, env) "
        "VALUES({}, '{}')".format(id, env)
    )
    update_local_db(
        "UPDATE favourite_tenants "
        "SET visit_count = visit_count + 1, "
        "visited = datetime('now') "
        "WHERE id = {} AND env = '{}'".format(
            id, env
        )
    )


def refresh_favourite_tenants(envs):
    env_list = list()
    for env in envs:
        env_list.append(env['name'])
    if env_list:
        update_local_db(
            "DELETE FROM favourite_tenants "
            "WHERE env NOT IN('{}')".format("','".join(env_list))
        )


def list_favourite_tenants(env, all_tenants, top=10):
    tenant_list = list()
    results = None
    for tenant in all_tenants:
        tenant_list.append(str(tenant['id']))
    if tenant_list:
        # 删除本地存储的无效商户
        sql = (
            "DELETE FROM favourite_tenants "
            "WHERE env = '{}' "
            "AND id NOT IN({})"
        ).format(env, ','.join(tenant_list))
        update_local_db(sql)
        # 查询
        results = query_local_db(
            "SELECT id FROM favourite_tenants "
            "WHERE env = '{}' "
            "ORDER BY visit_count DESC, visited DESC "
            "LIMIT {}".format(env, top)
        )
    return results


init_localdb()

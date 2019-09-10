import torch


def login(
    db_host, db_user, db_passwd,
    user, passwd
):
    conn = torch.connect(db_host, db_user, db_passwd, 'hephaestus')
    sql = (
        "CALL login('{}', '{}')"
    ).format(user, passwd)
    results = torch.update(conn, eval('["' + sql + '"]'))
    return results[0] if results else None


def get(
    db_host, db_user, db_passwd,
    id
):
    conn = torch.connect(db_host, db_user, db_passwd, 'hephaestus')
    sql = "SELECT `name`, dominated FROM gods WHERE id = {}".format(id)
    return torch.query(conn, sql)


def find_duplicate(
    db_host, db_user, db_passwd,
    username
):
    conn = torch.connect(db_host, db_user, db_passwd, 'hephaestus')
    sql = "SELECT `name` FROM gods WHERE `name` = '{}'".format(username)
    return torch.query(conn, sql)


def create(
    db_host, db_user, db_passwd,
    username, passwd, permission_list
):
    conn = torch.connect(db_host, db_user, db_passwd, 'hephaestus')
    sql = (
        "INSERT INTO gods(`name`, `secret`) "
        "VALUES(%s, SHA2(%s, 256))"
    )
    result = torch.execute(conn, sql, (username, passwd))  # 添加用户
    if result:
        # 添加用户权限
        pl = list()
        for p in permission_list:
            if p['permission'] != 0:
                pl.append((p['env'], p['permission']))
        conn = torch.connect(db_host, db_user, db_passwd, 'hephaestus')
        sql = (
            "INSERT INTO permission(island_name, god_id, access_level) "
            "VALUES(%s, %s, %s)"
        )
        return torch.execute_many(conn, sql, pl)
    else:
        return result

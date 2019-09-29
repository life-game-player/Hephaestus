import torch


def login(
    db_host, db_user, db_passwd,
    user, passwd
):
    conn = torch.connect(db_host, db_user, db_passwd, 'hephaestus')
    sql = (
        "CALL login('{}', '{}')"
    ).format(user, passwd)
    result, resultset = torch.call_proc_with_resultset(conn, sql)
    return resultset[0] if resultset else None


def get(
    db_host, db_user, db_passwd,
    id
):
    conn = torch.connect(db_host, db_user, db_passwd, 'hephaestus')
    sql = (
        "SELECT `id`, `name`, dominated, `status`, "
        "created, modified, last_login "
        "FROM gods "
        "WHERE id = {}"
    ).format(id)
    return torch.query(conn, sql)


def get_by_name(
    db_host, db_user, db_passwd,
    username
):
    conn = torch.connect(db_host, db_user, db_passwd, 'hephaestus')
    sql = (
        "SELECT `id`, `name`, dominated, `status`, "
        "created, modified, last_login "
        "FROM gods "
        "WHERE name = '{}'"
    ).format(username)
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
    if result == 0:
        new_user = get_by_name(db_host, db_user, db_passwd, username)
        if new_user and new_user[0]['id']:
            # 添加用户权限
            pl = []
            user_id = new_user[0]['id']
            for p in permission_list:
                if p['permission'] != 0:
                    pl.append((p['env'], user_id, p['permission']))
            conn = torch.connect(db_host, db_user, db_passwd, 'hephaestus')
            sql = (
                "INSERT INTO permission(island_name, god_id, access_level) "
                "VALUES(%s, %s, %s)"
            )
            return torch.execute_many(conn, sql, pl)
        else:
            return 1
    else:
        return 1


def list(
    db_host, db_user, db_passwd
):
    conn = torch.connect(db_host, db_user, db_passwd, 'hephaestus')
    sql = (
        "SELECT id, `name`, dominated FROM gods "
        "WHERE dominated = FALSE"
    )
    return torch.query(conn, sql)


def update_user_status(
    db_host, db_user, db_passwd,
    user_status, user_id
):
    conn = torch.connect(db_host, db_user, db_passwd, 'hephaestus')
    sql = (
        "UPDATE gods SET `status` = %s "
        "WHERE id = %s"
    )
    return torch.execute(conn, sql, (user_status, user_id))


def delete(
    db_host, db_user, db_passwd, user_id
):
    conn = torch.connect(db_host, db_user, db_passwd, 'hephaestus')
    sql = (
        "DELETE FROM gods WHERE id = %s"
    )
    return torch.execute(conn, sql, (user_id,))


def update_passwd(
    db_host, db_user, db_passwd, user_id, passwd
):
    conn = torch.connect(db_host, db_user, db_passwd, 'hephaestus')
    sql = (
        "UPDATE gods SET secret = SHA2(%s, 256) "
        "WHERE id = %s"
    )
    return torch.execute(conn, sql, (passwd, user_id))


def update_name(
    db_host, db_user, db_passwd, user_id, new_name
):
    conn = torch.connect(db_host, db_user, db_passwd, 'hephaestus')
    sql = (
        "UPDATE gods SET name = %s "
        "WHERE id = %s"
    )
    return torch.execute(conn, sql, (new_name, user_id))

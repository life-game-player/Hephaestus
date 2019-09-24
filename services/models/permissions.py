import torch


def get_by_user(db_host, db_user, db_passwd, user_id):
    conn = torch.connect(db_host, db_user, db_passwd, 'hephaestus')
    sql = (
        "SELECT island_name, access_level "
        "FROM permission "
        "WHERE god_id = {}"
    ).format(user_id)
    return torch.query(conn, sql)


def update_by_user(
    db_host, db_user, db_passwd,
    user_permisson, user_id
):
    result = 0
    for up in user_permisson:
        conn = torch.connect(db_host, db_user, db_passwd, 'hephaestus')
        if up['permission']:
            sql = (
                "INSERT INTO permission VALUES("
                "%s, %s, %s, NOW()"
                ") ON DUPLICATE KEY UPDATE "
                "access_level = %s"
            )
            params = (
                up['env'],
                user_id,
                up['permission'],
                up['permission']
            )
        else:
            sql = (
                "DELETE FROM permission "
                "WHERE island_name = %s AND god_id = %s"
            )
            params = (
                up['env'],
                user_id
            )
        result += torch.execute(conn, sql, params)
    return result

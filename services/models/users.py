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

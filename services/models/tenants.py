import torch


def list(db_host, db_user, db_passwd):
    conn = torch.connect(db_host, db_user, db_passwd, 'yeeoffice-management')
    sql = (
        "SELECT MerchantKey AS id, MerchantName AS `name` "
        "FROM merchant "
        "ORDER BY Created DESC"
    )
    return torch.query(conn, sql)

import torch


def list(db_host, db_user, db_passwd):
    conn = torch.connect(db_host, db_user, db_passwd, 'yeeoffice-management')
    sql = (
        "SELECT MerchantKey AS id, MerchantName AS `name` "
        "FROM merchant "
        "ORDER BY Created DESC"
    )
    return torch.query(conn, sql)


def get_tenant_db(db_host, db_user, db_passwd, tenant_id):
    conn = torch.connect(db_host, db_user, db_passwd, 'yeeoffice-management')
    sql = (
        "SELECT DISTINCT map.DatabaseName AS tenant_db "
        "FROM merchant m "
        "INNER JOIN merchantdbmapping map "
        "ON m.MerchantID = map.MerchantID "
        "WHERE m.MerchantKey = {}".format(tenant_id)
    )
    return torch.query(conn, sql)

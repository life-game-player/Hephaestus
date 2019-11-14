import torch


def list_root_instances(
    db_host, db_user, db_passwd, db_name,
    tenant_id, applicationid
):
    conn = torch.connect(db_host, db_user, db_passwd, db_name)
    sql = (
        "SELECT ProcInstID, `Name`, Created, Modified, `Status`, "
        "`Comment`"
        "FROM flowcraft_procinst "
        "WHERE TenantID = %s AND ApplicationID = %s "
        "AND ParentInstID = 0 "
        "ORDER BY Created DESC"
    )
    return torch.query_with_param(conn, sql, (tenant_id, applicationid))


def get(
    db_host, db_user, db_passwd, db_name,
    tenant_id, instance_id
):
    conn = torch.connect(db_host, db_user, db_passwd, db_name)
    sql = (
        "SELECT ProcInstID, `Name`, Created, Modified, `Status`, "
        "`Comment`"
        "FROM flowcraft_procinst "
        "WHERE TenantID = %s AND ProcInstID = %s "
    )
    return torch.query_with_param(conn, sql, (tenant_id, instance_id))

import torch


def list_by_procinstid(
    db_host, db_user, db_passwd, db_name,
    tenant_id, instance_id
):
    conn = torch.connect(db_host, db_user, db_passwd, db_name)
    sql = (
        "SELECT ActivityID "
        "FROM flowcraft_execution "
        "WHERE TenantID = %s AND ProcInstID = %s "
    )
    return torch.query_with_param(conn, sql, (tenant_id, instance_id))

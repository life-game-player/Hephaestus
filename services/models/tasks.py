import torch


def get(
    db_host, db_user, db_passwd, db_name,
    tenant_id, task_id
):
    conn = torch.connect(db_host, db_user, db_passwd, db_name)
    sql = (
        "SELECT TaskID, Name, StartTime, EndTime, "
        "DeleteReason, Outcome "
        "FROM flowcraft_task "
        "WHERE TenantID = %s AND TaskID = %s "
    )
    return torch.query_with_param(conn, sql, (tenant_id, task_id))

import torch


def list_by_procinstid(
    db_host, db_user, db_passwd, db_name,
    tenant_id, procinstid
):
    conn = torch.connect(db_host, db_user, db_passwd, db_name)
    sql = (
        "SELECT ActivityID, PrevAcitivtyID AS PrevActivityID, `Name`, "
        "ExecutionID, ActivityDefID, ProcDefID, CallProcInstID, TaskID, "
        "ActivityType, `Status`, Created, Modified "
        "FROM flowcraft_activity "
        "WHERE TenantID = %s AND ProcInstID = %s "
        "ORDER BY ActivityID, Created"
    )
    return torch.query_with_param(conn, sql, (tenant_id, procinstid))

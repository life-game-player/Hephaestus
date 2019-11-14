import torch


def list_by_keys(
    db_host, db_user, db_passwd, db_name,
    tenant_id, key_list
):
    conn = torch.connect(db_host, db_user, db_passwd, db_name)
    param = ",".join(['%s'] * len(key_list))
    sql = (
        "SELECT ApplicationID, DefKey AS validate_param "
        "FROM flowcraft_application "
        "WHERE TenantID = {} AND DefKey IN({})".format(
            tenant_id,
            param
        )
    )
    return torch.query_with_param(conn, sql, tuple(key_list))


def list_by_flownos(
    db_host, db_user, db_passwd, db_name,
    tenant_id, flowno_list
):
    conn = torch.connect(db_host, db_user, db_passwd, db_name)
    param = ",".join(['%s'] * len(flowno_list))
    sql = (
        "SELECT ApplicationID, FlowNo AS validate_param "
        "FROM flowcraft_application "
        "WHERE TenantID = {} AND FlowNo IN({})".format(
            tenant_id,
            param
        )
    )
    return torch.query_with_param(conn, sql, tuple(flowno_list))


def get_by_flowno(
    db_host, db_user, db_passwd, db_name,
    tenant_id, flowno
):
    conn = torch.connect(db_host, db_user, db_passwd, db_name)
    sql = (
        "SELECT a.ApplicationID, a.ApplicantUserID, "
        "u.name_cn AS ApplicantUserName, a.`Status`, a.DefKey, "
        "a.Created, a.Modified, a.`Comment` "
        "FROM flowcraft_application a "
        "LEFT JOIN yeeoffice_list_userinfo_data u "
        "ON a.ApplicantUserID = u.listdataid "
        "WHERE a.TenantID = %s AND a.FlowNo = %s"
    )
    return torch.query_with_param(conn, sql, (tenant_id, flowno))


def list_persistent_variables(
    db_host, db_user, db_passwd, db_name,
    tenant_id, applicationid
):
    conn = torch.connect(db_host, db_user, db_passwd, db_name)
    sql = (
        "SELECT `Name`, `Type`, `Value`, Created, Modified "
        "FROM flowcraft_variable "
        "WHERE TenantID = %s AND ApplicationID = %s "
        "ORDER BY `Name`"
    )
    return torch.query_with_param(conn, sql, (tenant_id, applicationid))


def list_runtime_variables(
    db_host, db_user, db_passwd, db_name,
    tenant_id, applicationid
):
    conn = torch.connect(db_host, db_user, db_passwd, db_name)
    sql = (
        "SELECT `Name`, `Type`, `Value`, Created, Modified "
        "FROM flowcraft_variableruntime "
        "WHERE TenantID = %s AND ApplicationID = %s "
        "ORDER BY `Name`"
    )
    return torch.query_with_param(conn, sql, (tenant_id, applicationid))


def delete(
    db_host, db_user, db_passwd, db_name,
    tenant_id, application_id_list
):
    conn = torch.connect(db_host, db_user, db_passwd, db_name)
    param = ",".join(['%s'] * len(application_id_list))
    list_sql = []

    list_sql.append(
        [
            (
                "DELETE t "
                "FROM flowcraft_task t "
                "INNER JOIN flowcraft_application a "
                "ON t.TenantID = a.TenantID AND t.FlowNo = a.FlowNo "
                "WHERE a.TenantID = {} AND a.ApplicationID IN({}) "
            ).format(tenant_id, param),
            tuple(application_id_list)
        ]
    )  # 删除关联任务
    list_sql.append(
        [
            (
                "DELETE tr "
                "FROM flowcraft_taskruntime tr "
                "INNER JOIN flowcraft_application a "
                "ON tr.TenantID = a.TenantID AND tr.FlowNo = a.FlowNo "
                "WHERE a.TenantID = {} AND a.ApplicationID IN({})"
            ).format(tenant_id, param),
            tuple(application_id_list)
        ]
    )  # 删除关联活动任务
    list_sql.append(
        [
            (
                "DELETE e "
                "FROM flowcraft_execution e "
                "INNER JOIN flowcraft_application a "
                "ON e.TenantID = a.TenantID "
                "AND e.ApplicationID = a.ApplicationID "
                "WHERE a.TenantID = {} AND a.ApplicationID IN({})"
            ).format(tenant_id, param),
            tuple(application_id_list)
        ]
    )  # 删除关联execution
    list_sql.append(
        [
            (
                "DELETE ac "
                "FROM flowcraft_activity ac "
                "INNER JOIN flowcraft_application a "
                "ON ac.TenantID = a.TenantID "
                "AND ac.ApplicationID = a.ApplicationID "
                "WHERE a.TenantID = {} AND a.ApplicationID IN({})"
            ).format(tenant_id, param),
            tuple(application_id_list)
        ]
    )  # 删除关联节点
    list_sql.append(
        [
            (
                "DELETE i "
                "FROM flowcraft_procinst i "
                "INNER JOIN flowcraft_application a "
                "ON i.TenantID = a.TenantID "
                "AND i.ApplicationID = a.ApplicationID "
                "WHERE a.TenantID = {} AND a.ApplicationID IN({})"
            ).format(tenant_id, param),
            tuple(application_id_list)
        ]
    )  # 删除关联实例
    list_sql.append(
        [
            (
                "DELETE FROM flowcraft_application "
                "WHERE TenantID = {} AND ApplicationID IN({})"
            ).format(tenant_id, param),
            tuple(application_id_list)
        ]
    )  # 删除流程记录
    list_sql.append(
        [
            (
                "DELETE FROM flowcraft_report_detail "
                "WHERE TenantID = {} AND ApplicationID IN({})"
            ).format(tenant_id, param),
            tuple(application_id_list)
        ]
    )  # 删除流程报表记录

    return torch.execute_list_with_param(conn, list_sql)

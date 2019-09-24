import torch


def create(
    host, user, passwd,
    module, operator, operation, result
):
    """
        Operation:
            1: Create
            2: Modify
            3: Query
            4: Delete

        Result:
            0: Succeeded
            1: Failed
    """
    conn = torch.connect(host, user, passwd, 'hephaestus')
    list_sql = list()
    list_sql.append(
        "INSERT INTO mnemosyne(module, operator, operation, result) "
        "VALUES('{}', {}, {}, {})".format(module, operator, operation, result)
    )
    torch.execute_list(conn, list_sql)

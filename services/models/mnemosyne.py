import torch


def create(
    host, user, passwd,
    operator, operation, result
):
    """
        Operation:
            1: Create

        Result:
            0: Succeeded
            1: Failed
    """
    conn = torch.connect(host, user, passwd, 'hephaestus')
    list_sql = list()
    list_sql.append(
        "INSERT INTO mnemosyne(operator, operation, result) "
        "VALUES({}, {}, {})".format(operator, operation, result)
    )
    torch.update(conn, list_sql)

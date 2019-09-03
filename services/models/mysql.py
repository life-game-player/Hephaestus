import torch
from clio import logger


def test(host, user, passwd, db='mysql'):
    result = 0
    try:
        conn = torch.connect(host, user, passwd, db)
        conn.close()
    except Exception as e:
        result = 1
        logger.error(
            "{} occured".format(type(e).__name__),
            exc_info=True
        )
    return result

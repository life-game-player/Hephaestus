import pymysql


def connect(host, user, password, db):
    return pymysql.connect(
        host=host,
        user=user,
        password=password,
        db=db
    )


def light_up(host, user, password):
    """
    Check if connection parameters are valid.
    """
    try:
        conn = connect(host, user, password, 'mysql')
        conn.close()
        return True, None
    except Exception as e:
        return False, e.args


def query(conn, sql):
    try:
        with conn.cursor(pymysql.cursors.DictCursor) as c:
            c.execute(sql)
            results = c.fetchall()
            return results
    except Exception as e:
        print(e.args)
        return None
    finally:
        conn.close()


def update(conn, list_sql):
    try:
        with conn.cursor() as c:
            for sql in list_sql:
                c.execute(sql)
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()


def seek_hera(conn):
    schema = query(
        conn,
        (
            "SELECT schema_name FROM information_schema.schemata "
            "WHERE schema_name = 'hephaestus'"
        )
    )
    if schema:
        # 数据库已存在
        return True
    else:
        return False


def reset_hera(host, user, password, dominated_pwd):
    conn = connect(host, user, password, 'hephaestus')
    sql = (
        "UPDATE gods "
        "SET secret = SHA2('{}', 256)"
        "WHERE dominated = TRUE"
    )
    update(conn, eval('["' + sql + '"]'))
    conn = connect(host, user, password, 'hephaestus')
    result = query(
        conn,
        "SELECT name FROM gods WHERE dominated = TRUE"
    )
    return result[0]['name'] if result else None


def set_fire(host, user, password, dominated_user, dominated_pwd):
    conn = connect(host, user, password, 'mysql')
    sql = (
        "CREATE DATABASE hephaestus "
        "DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci"
    )
    update(conn, eval('["' + sql + '"]'))
    conn = connect(host, user, password, 'hephaestus')
    list_sql = list()
    sql = (
        "CREATE TABLE gods("
        "id INT NOT NULL PRIMARY KEY AUTO_INCREMENT, "
        "`name` VARCHAR(50) NOT NULL, "
        "`secret` VARCHAR(100) NOT NULL, "
        "last_login DATETIME, "
        "failures_since_last_login INT NOT NULL DEFAULT 0, "
        "failures_since_last_login_today INT NOT NULL DEFAULT 0, "
        "dominated BIT NOT NULL DEFAULT FALSE, "
        "created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, "
        "modified TIMESTAMP NOT NULL "
        "DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP "
        ")"
    )
    list_sql.append(sql)
    sql = (
        "CREATE UNIQUE INDEX UK_name "
        "ON gods(`name`)"
    )
    list_sql.append(sql)
    sql = (
        "CREATE TABLE islands("
        "`name` VARCHAR(30) NOT NULL PRIMARY KEY, "
        "created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, "
        "modified TIMESTAMP NOT NULL ON UPDATE CURRENT_TIMESTAMP "
        ")"
    )
    list_sql.append(sql)
    sql = (
        "CREATE TABLE permission("
        "island_name VARCHAR(30) NOT NULL, "
        "god_name VARCHAR(50) NOT NULL, "
        "access_level INT NOT NULL COMMENT '1: Tagrag, 2: Lord, 3: King', "
        "created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP"
        ")"
    )
    list_sql.append(sql)
    sql = (
        "INSERT INTO gods(`name`, secret, dominated) "
        "VALUES('{}', SHA2('{}', 256), TRUE)"
    ).format(dominated_user, dominated_pwd)
    list_sql.append(sql)
    update(conn, list_sql)

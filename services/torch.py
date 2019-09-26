import pymysql

from clio import logger


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
    results = None
    try:
        with conn.cursor(pymysql.cursors.DictCursor) as c:
            c.execute(sql)
            results = c.fetchall()
    except Exception as e:
        logger.error(
            "{} occured".format(type(e).__name__),
            exc_info=True
        )
    finally:
        conn.close()
    return results


def execute_list(conn, list_sql):
    try:
        with conn.cursor() as c:
            for sql in list_sql:
                c.execute(sql)
        conn.commit()
        return 0
    except Exception as e:
        conn.rollback()
        logger.error(
            "{} occured".format(type(e).__name__),
            exc_info=True
        )
        return 1
    finally:
        conn.close()


def call_proc_with_resultset(conn, sql):
    try:
        with conn.cursor() as c:
            c.execute(sql)
            resultset = c.fetchall()
        conn.commit()
        return 0, resultset
    except Exception as e:
        conn.rollback()
        logger.error(
            "{} occured".format(type(e).__name__),
            exc_info=True
        )
        return 1, None
    finally:
        conn.close()


def execute(conn, sql, params=None):
    try:
        with conn.cursor() as c:
            if params:
                c.execute(sql, params)
            else:
                c.execute(sql)
        conn.commit()
        return 0
    except Exception as e:
        conn.rollback()
        logger.error(
            "{} occured".format(type(e).__name__),
            exc_info=True
        )
        return 1
    finally:
        conn.close()


def execute_many(conn, sql, params):
    try:
        with conn.cursor() as c:
            c.executemany(sql, params)
        conn.commit()
        return 0
    except Exception as e:
        conn.rollback()
        logger.error(
            "{} occured".format(type(e).__name__),
            exc_info=True
        )
        return 1
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
    ).format(dominated_pwd)
    execute(conn, sql)
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
    execute(conn, sql)
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
        "`status` INT NOT NULL DEFAULT 0 "
        "COMMENT '0:Normal, 1:Disabled', "
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
        "CREATE TABLE mnemosyne("
        "id BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT, "
        "module VARCHAR(100) NOT NULL, "
        "operator BIGINT NOT NULL, "
        "operation INT NOT NULL, "
        "result INT NOT NULL, "
        "created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP "
        ")"
    )
    list_sql.append(sql)
    sql = (
        "CREATE TABLE islands("
        "`name` VARCHAR(30) NOT NULL PRIMARY KEY, "
        "read_host VARCHAR(255), "
        "write_host VARCHAR(255) NOT NULL, "
        "user VARCHAR(255) NOT NULL, "
        "secret BLOB NOT NULL, "
        "guid VARCHAR(100) NOT NULL, "
        "vector BLOB NOT NULL, "
        "created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, "
        "modified TIMESTAMP NOT NULL ON UPDATE CURRENT_TIMESTAMP "
        ")"
    )
    list_sql.append(sql)
    sql = (
        "CREATE TABLE permission("
        "island_name VARCHAR(30) NOT NULL, "
        "god_id BIGINT NOT NULL, "
        "access_level INT NOT NULL "
        "COMMENT '1: Tagrag(r), 2: Lord(w), 3: King(m)', "
        "created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP "
        "ON UPDATE CURRENT_TIMESTAMP, "
        "PRIMARY KEY(island_name, god_id)"
        ")"
    )
    list_sql.append(sql)
    sql = (
        "CREATE FUNCTION CBC_ENCRYPT"
        "(_key VARCHAR(100), _plain VARCHAR(255), _vector BLOB) "
        "RETURNS BLOB "
        "BEGIN "
        "SET block_encryption_mode = 'aes-256-cbc';"
        "SET @key_str = SHA2(_key, 512);"
        "RETURN AES_ENCRYPT(_plain, @key_str, _vector);"
        "END"
    )
    list_sql.append(sql)
    sql = (
        "CREATE FUNCTION CBC_DECRYPT"
        "(_key VARCHAR(100), _crypt BLOB, _vector BLOB) "
        "RETURNS VARCHAR(255)"
        "BEGIN "
        "SET block_encryption_mode = 'aes-256-cbc';"
        "SET @key_str = SHA2(_key, 512);"
        "RETURN AES_DECRYPT(_crypt, @key_str, _vector);"
        "END"
    )
    list_sql.append(sql)
    sql = (
        "CREATE PROCEDURE login(_user VARCHAR(50), _passwd VARCHAR(100)) "
        "BEGIN "
        "SET @id = NULL; "
        "SET @secret = NULL; "
        "SET @input_secret = SHA2(_passwd, 256); "
        "SET @status = 0; "
        "SELECT id, secret, `status` INTO @id, @secret, @status FROM gods "
        "WHERE name = _user; "
        "IF @id IS NOT NULL AND @status = 0 THEN "
        "UPDATE gods "
        "SET last_login = IF(@secret = @input_secret, NOW(3), last_login), "
        "failures_since_last_login = "
        "IF(@secret = @input_secret, 0, failures_since_last_login + 1), "
        "failures_since_last_login_today = "
        "IF(CAST(NOW() AS DATE) > CAST(modified AS DATE), "
        "0, failures_since_last_login_today), "
        "failures_since_last_login_today = "
        "IF(@secret = @input_secret, 0, failures_since_last_login_today + 1), "
        "`status` = IF(failures_since_last_login_today > 6, 1, `status`) "
        "WHERE id = @id; "
        "END IF; "
        "SELECT IF(@secret = @input_secret, @id, NULL) AS id, "
        "@status AS `status`;"
        "END"
    )
    list_sql.append(sql)
    sql = (
        "INSERT INTO gods(`name`, secret, dominated) "
        "VALUES('{}', SHA2('{}', 256), TRUE)"
    ).format(dominated_user, dominated_pwd)
    list_sql.append(sql)
    execute_list(conn, list_sql)

import logging
import mysql
import yaml
from mysql import connector

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger("MySQL_Driver_Error")
logger_mysql = logging.getLogger("MySQL_Driver")

with open("config.yaml", "r"):
    with open('config.yaml', 'r') as file:
        loadedfile = yaml.safe_load(file)
        MySQLHOST = loadedfile['mysql_ip']
        MySQLPORT = loadedfile['mysql_port']
        MySQLUSER = loadedfile['mysql_user']
        MySQLPASS = loadedfile['mysql_password']
        MySQLDATABASE = loadedfile['mysql_general_database']

DB = mysql.connector.connect(
    host=MySQLHOST,
    port=MySQLPORT,
    user=MySQLUSER,
    password=MySQLPASS,
    database=MySQLDATABASE)


def startdbs():
    try:
        DB.connect()
    except Exception as e:
        logger.error(f"Помилка при підключенні основної бази данних.\nВиключення: {e}")
        return False
    else:
        logger_mysql.info("Основна база данних підключена!")
    return True


def closedbs():
    try:
        DB.connect()
    except Exception as e:
        logger.error(f"Помилка при відключенні основної бази данних.\nВиключення: {e}")
        return False
    else:
        logger_mysql.info("Основна база данних відключена!")


def sendSQL(sql):
    cursor = DB.cursor()
    try:
        cursor.execute(sql)
    except Exception as e:
        logger.exception(f"Виникла помилка в функції sendSQL. DEBUG:\nSQL: {sql}\nException: {e}")


def executeSQL(sql):
    cursor = DB.cursor()
    try:
        cursor.execute(sql)
    except Exception as e:
        logger.exception(f"Виникла помилка в функції executeSQL. DEBUG:\nSQL: {sql}\nException: {e}")
    else:
        return cursor


def DBCommit():
    try:
        DB.commit()
    except Exception as e:
        logger.exception(f"Виникла помилка в функції DBCommit. DEBUG:\nException: {e}")

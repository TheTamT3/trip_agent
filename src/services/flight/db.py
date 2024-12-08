import mysql.connector
from mysql.connector import Error

from src._settings import settings


def create_connection():
    try:
        connection = mysql.connector.connect(
            host=settings.MYSQL_HOST, user=settings.MYSQL_USER, password=settings.MYSQL_PASSWORD, database=settings.MYSQL_NAME
        )
        return connection
    except Error as e:
        raise e


def close_connection(connection):
    if connection.is_connected():
        connection.close()

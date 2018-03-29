# coding=utf-8

import MySQLdb
from libs.const.mysql import *


def connect_mysql():
    conn = MySQLdb.connect(host=MYSQL_HOST, port=MYSQL_PORT, user=MYSQL_USER, passwd=MYSQL_PASSWORD, db=MYSQL_DB)
    conn.ping(True)
    return conn

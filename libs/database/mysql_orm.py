# coding=utf-8
"""
operate mysql database vis ORM lib
only define base class
place your table definition to module dir

__author__ = 'zengyuetian'

reference: http://docs.sqlalchemy.org/en/latest/orm/tutorial.html

"""

from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base
from libs.const.mysql import *

# describing the database tables we’ll be dealing with,
# and then by defining our own classes which will be mapped to those tables.
Base = declarative_base()

DB_CONNECT_STRING = 'mysql+mysqldb://{0}:{1}@{2}:{3}/{4}'.\
    format("root", "", MYSQL_HOST, MYSQL_PORT, MYSQL_DB)


class MysqlORM(object):
    def __init__(self):
        self.engine = create_engine(DB_CONNECT_STRING, echo=False, echo_pool=False, pool_size=0)
        session_factory = sessionmaker(bind=self.engine)
        self.session = scoped_session(session_factory)
        # self.DBSession = sessionmaker(bind=self.engine)
        # self.session = self.DBSession()

    def create_tables(self):
        Base.metadata.create_all(self.engine)

    def drop_tables(self):
        Base.metadata.drop_all(self.engine)

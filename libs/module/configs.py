# coding=utf-8
# config table
# __author__ = JinYiFan

from libs.database.mysql_orm import *


class Configs(Base):
    __tablename__ = "configs"
    role = Column(String, primary_key=True)
    content = Column(Integer, primary_key=True)

    def __init__(self, role, content):
        self.role = role
        self.content = content

if __name__ == "__main__":
    orm = MysqlORM()
    results = orm.session.query(Configs).all()
    print type(results)
    for result in results:
        print result.role, result.content

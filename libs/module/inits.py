# coding=utf-8
# init table
# __author__ = JinYiFan

from libs.database.mysql_orm import *


class Inits(Base):
    __tablename__ = "inits"
    role = Column(String, primary_key=True)
    num = Column(Integer)

    def __init__(self, role, num):
        self.role = role
        self.num = num

if __name__ == "__main__":
    orm = MysqlORM()
    results = orm.session.query(Inits).all()
    print type(results)
    for result in results:
        print result.role, result.num

# coding=utf-8
# live_files table
# __author__ = JinYiFan

from libs.database.mysql_orm import *


class Live_File(Base):
    __tablename__ = "live_files"
    file_id = Column(String, primary_key=True)
    ppc = Column(Integer, primary_key=False)
    cppc = Column(Integer, primary_key=False)
    url = Column(String, primary_key=False)

    def __init__(self, file_id, ppc, cppc, url):
        self.file_id = file_id
        self.ppc = ppc
        self.cppc = cppc
        self.url = url


if __name__ == "__main__":
    orm = MysqlORM()
    results = orm.session.query(Live_File).all()
    # print type(results)
    for result in results:
        print result.file_id

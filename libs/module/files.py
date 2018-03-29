# coding=utf-8
# files table
# __author__ = JinYiFan

from libs.database.mysql_orm import *


class File(Base):
    __tablename__ = "files"
    file_id = Column(String, primary_key=True)
    file_size = Column(Integer, primary_key=False)
    url = Column(String, primary_key=False)
    ppc = Column(Integer, primary_key=False)
    cppc = Column(Integer, primary_key=False)
    piece_size = Column(Integer, primary_key=False)

    def __init__(self, file_id, file_size, url, ppc, cppc, piece_size):
        self.file_id = file_id
        self.file_size = file_size
        self.url = url
        self.ppc = ppc
        self.cppc = cppc
        self.piece_size = piece_size


if __name__ == "__main__":
    orm = MysqlORM()
    results = orm.session.query(File).all()
    # print type(results)
    for result in results:
        print result.file_id

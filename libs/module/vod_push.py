# coding=utf-8
# vod_push table
# __author__ = JinYiFan

from libs.database.mysql_orm import *


class Vod_Push(Base):
    __tablename__ = "vod_push"
    push_id = Column(String, primary_key=True)
    push_ip = Column(String, primary_key=False)
    disk_size = Column(Integer, primary_key=False)
    lsm_used = Column(Integer, primary_key=False)
    lsm_free = Column(Integer, primary_key=False)

    # content = Column(Integer)

    def __init__(
            self,
            push_id=None,
            push_ip=None,
            disk_size=None,
            lsm_used=None,
            lsm_free=None):
        self.push_id = push_id
        self.push_ip = push_ip
        self.disk_size = disk_size
        self.lsm_used = lsm_used
        self.lsm_free = lsm_free


if __name__ == "__main__":
    orm = MysqlORM()
    results = orm.session.query(Vod_Push).all()
    # print type(results)
    for result in results:
        print result.push_id

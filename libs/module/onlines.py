# coding=utf-8
# online table
# __author__ = JinYiFan

from libs.database.mysql_orm import *


class Online(Base):
    __tablename__ = "online"
    id = Column(Integer, primary_key=True)
    peer_id = Column(String, primary_key=False)
    sdk_version = Column(String, primary_key=False)
    public_ip = Column(String, primary_key=False)
    public_port = Column(Integer, primary_key=False)
    private_ip = Column(String, primary_key=False)
    private_port = Column(Integer, primary_key=False)
    nat_type = Column(Integer, primary_key=False)
    stun_ip = Column(String, primary_key=False)
    isp_id = Column(String, primary_key=False)
    province_id = Column(String, primary_key=False)
    lsm_free = Column(Integer, primary_key=False)
    lsm_total = Column(Integer, primary_key=False)
    disk_total = Column(Integer, primary_key=False)
    disk_free = Column(Integer, primary_key=False)

    def __init__(
            self,
            id=None,
            peer_id=None,
            sdk_version=None,
            public_ip=None,
            public_port=None,
            private_ip=None,
            private_port=None,
            nat_type=None,
            stun_ip=None,
            isp_id=None,
            province_id=None,
            file_id=None,
            file_status=None,
            lsm_free=None,
            lsm_total=None,
            disk_total=None,
            disk_free=None,
    ):
        self.id = id
        self.peer_id = peer_id
        self.sdk_version = sdk_version
        self.public_ip = public_ip
        self.public_port = public_port
        self.private_ip = private_ip
        self.private_port = private_port
        self.nat_type = nat_type
        self.stun_ip = stun_ip
        self.isp_id = isp_id
        self.province_id = province_id
        self.file_id = file_id
        self.file_status = file_status
        self.lsm_free = lsm_free
        self.lsm_total = lsm_total
        self.disk_total = disk_total
        self.disk_free = disk_free


if __name__ == "__main__":
    orm = MysqlORM()
    results = orm.session.query(Online).all()
    # print type(results)
    for result in results:
        print result.lsm_free, type(result.lsm_free)

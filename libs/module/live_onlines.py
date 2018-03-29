# coding=utf-8
# live_online table
# __author__ = Su Qi

from libs.database.mysql_orm import *


class Live_Online(Base):
    __tablename__ = "live_online"
    id = Column(Integer, primary_key=True)
    peer_id = Column(String, primary_key=False)
    sdk_version = Column(String, primary_key=False)
    nat_type = Column(Integer, primary_key=False)
    public_ip = Column(String, primary_key=False)
    public_port = Column(Integer, primary_key=False)
    private_ip = Column(String, primary_key=False)
    private_port = Column(Integer, primary_key=False)
    province_id = Column(String, primary_key=False)
    country = Column(String, primary_key=False)
    city_id = Column(String, primary_key=False)
    ssid = Column(String, primary_key=False)
    isp_id = Column(String, primary_key=False)
    cppc = Column(Integer, primary_key=False)
    # ifsid = Column(String, primary_key=False)
    # uid_index = Column(Integer, primary_key=False)

    def __init__(
            self,
            id=None,
            peer_id=None,
            sdk_version=None,
            nat_type=None,
            public_ip=None,
            public_port=None,
            private_ip=None,
            private_port=None,
            province_id=None,
            country=None,
            city_id=None,
            ssid=None,
            isp_id=None,
            cppc=None
            # ifsid=None,
            # uid_index=None
    ):
        self.id = id
        self.peer_id = peer_id
        self.sdk_version = sdk_version
        self.nat_type = nat_type
        self.public_ip = public_ip
        self.public_port = public_port
        self.private_ip = private_ip
        self.private_port = private_port
        self.province_id = province_id
        self.country = country
        self.city_id = city_id
        self.ssid = ssid
        self.isp_id = isp_id
        self.cppc = cppc
        # self.ifsid = ifsid
        # self.uid_index = uid_index


if __name__ == "__main__":
    orm = MysqlORM()
    results = orm.session.query(Live_Online).all()
    # print type(results)
    for result in results:
        print result.lsm_free, type(result.lsm_free)

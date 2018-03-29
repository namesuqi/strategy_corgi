# coding=utf-8
# live_peer table
# __author__ = Su Qi

from libs.database.mysql_orm import *


class Live_Peer(Base):
    __tablename__ = "live_peer"
    id = Column(Integer, primary_key=True)
    peer_id = Column(String, primary_key=False)
    version = Column(String, primary_key=False)
    country = Column(String, primary_key=False)
    province_id = Column(String, primary_key=False)
    city_id = Column(String, primary_key=False)
    isp_id = Column(String, primary_key=False)
    file_id = Column(String, primary_key=False)
    chunk_id = Column(INTEGER, primary_key=False)
    operation = Column(String, primary_key=False)
    cdn = Column(Integer, primary_key=False)
    p2p = Column(Integer, primary_key=False)
    ssid = Column(Integer, primary_key=False)
    p2penable = Column(String, primary_key=False)

    def __init__(
            self,
            peer_id,
            version,
            country,
            province_id,
            city_id,
            isp_id,
            file_id,
            chunk_id,
            operation,
            cdn,
            p2p,
            ssid,
            p2penable
    ):
        self.peer_id = peer_id
        self.version = version
        self.country = country
        self.province_id = province_id
        self.city_id = city_id
        self.isp_id = isp_id
        self.file_id = file_id
        self.chunk_id = chunk_id
        self.operation = operation
        self.cdn = cdn
        self.p2p = p2p
        self.ssid = ssid
        self.p2penable = p2penable


if __name__ == "__main__":
    orm = MysqlORM()
    results = orm.session.query(Live_Peer).all()
    # print type(results)
    for result in results:
        print result.seeds_download

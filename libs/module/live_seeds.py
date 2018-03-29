# coding=utf-8
# live_seed table
# __author__ = Su Qi

from libs.database.mysql_orm import *


class Live_Seed(Base):
    __tablename__ = "live_seed"
    id = Column(Integer, primary_key=True)
    peer_id = Column(String, primary_key=False)
    version = Column(String, primary_key=False)
    country = Column(String, primary_key=False)
    province_id = Column(String, primary_key=False)
    city_id = Column(String, primary_key=False)
    isp_id = Column(String, primary_key=False)
    file_id = Column(String, primary_key=False)
    cppc = Column(Integer, primary_key=False)
    operation = Column(String, primary_key=False)
    upload = Column(Integer, primary_key=False)
    download = Column(Integer, primary_key=False)
    ssid = Column(String, primary_key=False)
    # lfsid = Column(String, primary_key=False)
    # uid_index = Column(String, primary_key=False)

    def __init__(
            self,
            peer_id=None,
            version=None,
            country=None,
            province_id=None,
            city_id=None,
            isp_id=None,
            file_id=None,
            cppc=None,
            operation=None,
            upload=None,
            download=None,
            ssid=None,
            # lfsid=None,
            # uid_index=None
    ):
        self.peer_id = peer_id
        self.version = version
        self.country = country
        self.province_id = province_id
        self.city_id = city_id
        self.isp_id = isp_id
        self.file_id = file_id
        self.cppc = cppc
        self.operation = operation
        self.upload = upload
        self.download = download
        self.ssid = ssid
        # self.lfsid = lfsid
        # self.uid_index = uid_index


if __name__ == "__main__":
    orm = MysqlORM()
    results = orm.session.query(Live_Seed).all()
    # print type(results)
    for result in results:
        print result.peer_id

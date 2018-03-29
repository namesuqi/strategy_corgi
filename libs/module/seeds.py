# coding=utf-8
# seed table
# __author__ = JinYiFan

from libs.database.mysql_orm import *


class Seed(Base):
    __tablename__ = "seed"
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

    file_id = Column(String, primary_key=False)
    file_status = Column(String, primary_key=False)
    lsm_free = Column(Integer, primary_key=False)
    lsm_total = Column(Integer, primary_key=False)
    disk_total = Column(Integer, primary_key=False)
    disk_free = Column(Integer, primary_key=False)
    duration = Column(Integer, primary_key=False)
    seeds_download = Column(Integer, primary_key=False)
    seeds_upload = Column(Integer, primary_key=False)
    cdn_download = Column(Integer, primary_key=False)
    p2p_download = Column(Integer, primary_key=False)
    operation = Column(String, primary_key=False)
    play_type = Column(String, primary_key=False)
    error_type = Column(String, primary_key=False)
    priority = Column(Integer, primary_key=False)
    file_size = Column(Integer, primary_key=False)
    file_url = Column(String, primary_key=False)
    ppc = Column(Integer, primary_key=False)
    cppc = Column(Integer, primary_key=False)
    piece_size = Column(Integer, primary_key=False)
    push_ip = Column(Integer, primary_key=False)
    push_port = Column(Integer, primary_key=False)

    # timestamp = Column(Integer, primary_key=False)

    def __init__(
            self,
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
            priority=None,
            duration=None,
            seeds_download=None,
            seeds_upload=None,
            cdn_download=None,
            p2p_download=None,
            operation=None,
            play_type=None,
            error_type=None,
            file_size=None,
            file_url=None,
            ppc=None,
            cppc=None,
            piece_size=None,
            push_ip=None,
            push_port=None
    ):
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
        self.duration = duration
        self.seeds_download = seeds_download
        self.seeds_upload = seeds_upload
        self.cdn_download = cdn_download
        self.p2p_download = p2p_download
        self.operation = operation
        self.play_type = play_type
        self.error_type = error_type
        self.priority = priority
        self.file_size = file_size
        self.file_url = file_url
        self.ppc = ppc
        self.cppc = cppc
        self.piece_size = piece_size
        self.push_ip = push_ip
        self.push_port = push_port
        # self.timestamp = timestamp
        # self.content = content


if __name__ == "__main__":
    orm = MysqlORM()
    results = orm.session.query(Seed).all()
    # print type(results)
    for result in results:
        print result.peer_id

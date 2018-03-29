# coding=utf-8
# peer table
# __author__ = JinYiFan

from libs.database.mysql_orm import *


class Peer(Base):
    __tablename__ = "peer"
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
    file_size = Column(Integer, primary_key=False)
    url = Column(String, primary_key=False)
    ppc = Column(Integer, primary_key=False)
    cppc = Column(Integer, primary_key=False)
    piece_size = Column(Integer, primary_key=False)
    duration = Column(String, primary_key=False)
    seeds_download = Column(Integer, primary_key=False)
    seeds_upload = Column(Integer, primary_key=False)
    cdn_download = Column(Integer, primary_key=False)
    p2p_download = Column(Integer, primary_key=False)
    operation = Column(String, primary_key=False)
    play_type = Column(String, primary_key=False)
    error_type = Column(String, primary_key=False)
    # content = Column(Integer)

    def __init__(self, peer_id, sdk_version, public_ip, public_port, private_ip, private_port, nat_type, stun_ip,
                 isp_id, province_id, file_id, duration, seeds_download, seeds_upload, cdn_download,
                 p2p_download, operation, play_type, error_type, file_size, url, ppc, cppc, piece_size):
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
        self.duration = duration
        self.seeds_download = seeds_download
        self.seeds_upload = seeds_upload
        self.cdn_download = cdn_download
        self.p2p_download = p2p_download
        self.operation = operation
        self.play_type = play_type
        self.error_type = error_type
        self.file_size = file_size
        self.url = url
        self.ppc = ppc
        self.cppc = cppc
        self.piece_size = piece_size
        # self.content = content


if __name__ == "__main__":
    orm = MysqlORM()
    results = orm.session.query(Peer).all()
    # print type(results)
    for result in results:
        print result.seeds_download

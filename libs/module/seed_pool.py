# coding=utf-8
# seed_pool table
# __author__ = 'myn'

from libs.database.mysql_orm import *


class Seed_pool(Base):
    __tablename__ = "seed_pool"
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
    ppc = Column(Integer, primary_key=False)
    cppc = Column(Integer, primary_key=False)
    file_id = Column(String, primary_key=False)

    def __init__(
            self,
            peer_id,
            sdk_version,
            public_ip,
            public_port,
            private_ip,
            private_port,
            nat_type,
            stun_ip,
            isp_id,
            province_id,
            ppc,
            cppc,
            file_id):
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
        self.ppc = ppc
        self.cppc = cppc
        self.file_id = file_id

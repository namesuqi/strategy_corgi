# coding=utf-8
# live_push table
# __author__ = JinYiFan

from libs.database.mysql_orm import *


class Live_Push(Base):
    __tablename__ = "live_push"
    host_id = Column(String, primary_key=True)
    ip = Column(String, primary_key=False)
    livepush_version = Column(String, primary_key=False)
    name = Column(String, primary_key=False)
    receive = Column(Integer, primary_key=False)
    transmit = Column(Integer, primary_key=False)
    bandwidth = Column(Integer, primary_key=False)
    cpu_count = Column(Integer, primary_key=False)
    cpu_load_1m = Column(String, primary_key=False)
    puff_thread_count = Column(Integer, primary_key=False)
    supp_thread_count = Column(Integer, primary_key=False)
    livepush_cpu_used_percentage = Column(String, primary_key=False)
    mem_total = Column(Integer, primary_key=False)
    mem_used = Column(Integer, primary_key=False)
    livepush_mem_used_percentage = Column(String, primary_key=False)
    event = Column(VARCHAR, primary_key=False)
    reason = Column(VARCHAR, primary_key=False)

    def __init__(
            self,
            host_id=None,
            ip=None,
            livepush_version=None,
            name=None,
            receive=None,
            transmit=None,
            bandwidth=None,
            cpu_count=None,
            cpu_load_1m=None,
            puff_thread_count=None,
            supp_thread_count=None,
            livepush_cpu_used_percentage=None,
            mem_total=None,
            mem_used=None,
            livepush_mem_used_percentage=None,
            event=None,
            reason=None):
        self.host_id = host_id
        self.ip = ip
        self.livepush_version = livepush_version
        self.name = name
        self.receive = receive
        self.transmit = transmit
        self.bandwidth = bandwidth
        self.cpu_count = cpu_count
        self.cpu_load_1m = cpu_load_1m
        self.puff_thread_count = puff_thread_count
        self.supp_thread_count = supp_thread_count
        self.livepush_cpu_used_percentage = livepush_cpu_used_percentage
        self.mem_total = mem_total
        self.mem_used = mem_used
        self.livepush_mem_used_percentage = livepush_mem_used_percentage
        self.event = event
        self.reason = reason


if __name__ == "__main__":
    orm = MysqlORM()
    results = orm.session.query(Live_Push).all()
    # print type(results)
    for result in results:
        print result.push_id

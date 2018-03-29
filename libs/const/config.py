# coding=utf-8
# config information
# __author__ = JinYiFan

import random
import time
from libs.module.peers import *
from libs.module.files import *
from libs.module.seeds import *

# vod_push lsm(B)
PUSH_ID = ["00:16:3E:06:C3:A6", "00:16:3E:06:C4:A7"]
PUSH_IP = ["118.190.153.230", "112.190.153.230"]
DISK_SIZE = 0
PUSH_LSM_USED = [160867237888, 12867237888]
PUSH_LSM_FREE = [30000000000000000, 32300000000000000]

# file
FILE_STATUS_1 = 'downloading'
FILE_STATUS_2 = 'done'
PPC = 304
CPPC = 1
PSIZE = 1396
DURATION = 60

BEHAVIOR = "in"
FLAG = "downloading"


# timestamp
t = time.time()
TIMESTAMP = int(round(t * 1000))

# SDK
STUN_IP = '192.168.1.202'
ISP_ID = '0'
PROVINCE_ID = '0'


# sdk disk and lsm(B)
def create_disk():
    disk_total = random.randint(70000000000, 90000000000)
    disk_free = random.randint(50000000000, 70000000000)
    # lsm_total = random.randint(700000000, 900000000)
    lsm_total = 524288000
    lsm_free = random.randint(6710886400, 7710886400)
    return disk_total, disk_free, lsm_total, lsm_free

disk_total, disk_free, lsm_total, lsm_free = create_disk()

DISK_TOTAL = 42139451392
DISK_FREE = 29080141824
LSM_TOTAL = 5242880000
LSM_FREE = 4274545760


# sdk flow
def flow():
    orm = MysqlORM()
    peer_count = len(orm.session.query(Peer).all())

    for file in orm.session.query(File).all():
        file_seed_count = orm.session.query(func.count('*')).filter(Seed.file_id == file.file_id,
                                                                    Seed.file_status == "done").scalar()
        PER_PEER_DOWNLOAD_ALL = file.file_size
        orm.session.close()

        per_peer_p2p_download = min(PER_PEER_DOWNLOAD_ALL * file_seed_count / file.ppc, PER_PEER_DOWNLOAD_ALL)
        per_peer_cdn_download = PER_PEER_DOWNLOAD_ALL - per_peer_p2p_download
        per_seed_download = int(PER_PEER_DOWNLOAD_ALL / file.ppc)

        if file_seed_count != 0:
            per_seed_upload = int(per_peer_p2p_download * peer_count / file_seed_count)
        else:
            per_seed_upload = 0
        orm.session.close()
        return per_peer_p2p_download, per_peer_cdn_download, per_seed_download, per_seed_upload

SEEDS_DOWNLOAD = 112345
SEEDS_UPLOAD = 112345
CDN_DOWNLOAD = 100000
P2P_DOWNLOAD = 12345

OPERATION = 'download'
PLAY_TYPE = 'vod'
ERROR_TYPE = 'NA'
PRIORITY = 1

# strategy_executor parameter
# distinguish between different tasks
PUSH_DEL_LEN = 6
PUSH_PREFETCH_LEN = 13
SDK_DEL_LEN = 7
SDK_DOWNLOAD_LEN = 14
# -----
PUSH_CONCURRENT_VOLUME = 100
# -----
# kafka address
KAFKA_ADDRESS = '192.168.4.230:9092'
# ------
# sdk lsm_free level
LSM_FREE_LEVEL_A = "A:lsm<=10"
LSM_FREE_LEVEL_B = "B:10<lsm<=50"
LSM_FREE_LEVEL_C = "C:50<lsm<=100"
LSM_FREE_LEVEL_D = "D:100<lsm<=300"
LSM_FREE_LEVEL_E = "E:300<lsm<=600"
LSM_FREE_LEVEL_F = "F:lsm>600"

# write log number
PUSH_WRITE_NUMBER = 1
FILE_WRITE_NUMBER = 10
FILE_STATUS_WRITE_NUMBER = 300
SDK_WRITE_NUMBER = 5000

if __name__ == '__main__':
    flow()

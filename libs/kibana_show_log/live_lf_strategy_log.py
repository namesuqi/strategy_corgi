#!/usr/bin/python
# coding=utf-8
# author: Su Qi
# read live_lf_strategy_log from LF_strategy and write to logs for ELK analysis

import paramiko
from libs.common.path import *
from libs.kibana_show_log.kibana_analyse_log import path_exists
import time
import re
import json

hostname = "192.168.1.188"
port = 22
username = "root"
password = "root"


def read_lf_strategy_log():
    # connection linux machine
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname, port, username, password, compress=True)
    sftp_client = client.open_sftp()
    # linux file path
    remote_file = sftp_client.open("/root/dslive/lf_strategy.out111")

    path_exists(LOGS_PATH)
    lf_strategy_log = LOGS_PATH + "/live_lf_strategy.log"
    fil = open(lf_strategy_log, "w")

    while True:
        try:
            for line in remote_file:
                if "delete" in line:
                    line_dict = line[2:-2]
                    print line_dict
                    line_list = '\n'.join(line_dict[i:i + 147] for i in range(0, len(line_dict), 147))
                    str_line = line_list.encode('unicode-escape').decode('string_escape')
                    timestamp = long(str_line.split(",", 4)[0].split(":")[1])
                    delete_peer_id = str(str_line.split(",", 4)[2].split(":")[1])[2:-1]
                    delete_file_id = str(str_line.split(",", 4)[3].split(":")[1])[2:-2]
                    lf_delete_count = {
                        "timestamp": timestamp,
                        "peer_id": delete_peer_id,
                        "file_id": delete_file_id
                    }
                    print lf_delete_count
                #     sdk_delete_count_json = json.dumps(sdk_delete_count_combine)
                #     fil.write(sdk_delete_count_json + "\n")
                # fil.flush()
        except Exception as e:
            print e.message

if __name__ == '__main__':
    from libs.module.live_peers import *
    orm = MysqlORM()
    aim = orm.session.query(Live_Peer).all()
    for p in orm.session.execute("select * from live_peer;"):
        print p
    orm.session.commit()
    orm.session.close()

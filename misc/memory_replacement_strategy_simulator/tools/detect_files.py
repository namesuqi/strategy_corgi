# detects files on vod_push disk for used in the configuration file
# author: myn

import paramiko

hostname = ''
user = ''
password = ''
cmd = 'cd /root/corgi/logs ;ls -l | awk  -F \' \' \'{print $5"\t"$9 }\''


def detect_files():
    conn = paramiko.SSHClient()
    conn.load_system_host_keys()
    conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    conn.connect(hostname=hostname, username=user, password=password)
    stdin, stdout, stderr = conn.exec_command(cmd)
    files_info_list = stdout.readlines()
    conn.close()
    return files_info_list


if __name__ == '__main__':
    # loader = Loader()
    # config_info = loader.load_config_file()
    # push_host = config_info['push_host']
    # push_user = config_info['user']
    # push_password = config_info['password']
    # files_info = detect_files('192.168.3.217', 'root', 'root')
    # print files_info
    # for f in files_info:
    #     print len(f.split(' ')), f.split(' ')
    l = [[u'\t\n', u'0\tvod_heartbeat.log\n'], 0]
    # for i in l:
    a = str(l[0][1]).strip('\n')
    print a
    print a.split('\t')



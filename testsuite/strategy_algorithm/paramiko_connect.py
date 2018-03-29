# coding=utf-8

import paramiko

# HOST_IP = "192.168.4.235"
HOST_IP = "192.168.3.190"
PORT = 22
USERNAME = "root"
PASSWORD = "root"


def sftp_connect():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOST_IP, PORT, USERNAME, PASSWORD, compress=True)
    ftp_client = client.open_sftp()
    return ftp_client


if __name__ == '__main__':
    sftp_connect()

# coding= utf-8
import requests
import threading
import time


def delayrun():
    print 'running'


if __name__ == '__main__':
    r = requests.get(
        "http://192.168.4.230:8081/subjects/live_report-value/versions/latest")
    if r.status_code == 200:
        rsp = r.json()
        print rsp["schema"]
        # print rsp["id"]

    t = threading.Timer(1, delayrun)
    t.start()
    while True:
        time.sleep(0.1)
        print 'main running'

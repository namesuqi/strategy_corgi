# coding=utf-8
import threading
import urllib2
import time
from log import Log

timer = []
log = Log('log', 'sdk_faker.log')
file_size = 1000
file_id = '561B90A24D754AC6FAFF7D3A54E9DA2A'
ppc = 304
chunks_per_query = 12
cppc = 1
push_host = '192.168.4.181:9529'
chunk_gross = 2400


def fake_sdk():
    global timer
    do_sdk_urls = []
    timer.sort(key=lambda x: x[1])
    for sdk in timer:
        if sdk[1] == timer[0][1]:
            get_file_url = \
                "http://{0}/push/files/{1}/chunks/{2}_{3}/pieces/{4}".format(
                    push_host, file_id, sdk[3], chunks_per_query, cppc)
            do_sdk_urls.append([sdk, get_file_url])
        # urls.append(get_file_url)
    time.sleep(do_sdk_urls[0][0][2])
    if do_sdk_urls[0][0][3] < chunk_gross:
        tds = []
        i = 0
        for do_sdk_url in do_sdk_urls:
            thread = threading.Thread(target=t, args=(do_sdk_url, i))
            i += 1
            tds.append(thread)
        for td in tds:
            td.start()
        for td in tds:
            td.join()
    else:
        exit(0)
    print 'zzzzzzzzzzzzzzzzzzzzzzzz'
    fake_sdk()


def t(do_sdk_url, i):
    global timer
    req = urllib2.Request(do_sdk_url[1])
    try:
        response = urllib2.urlopen(req)
        if response.getcode() == 200:
            mutex.acquire()
            timer[i][3] += 12
            timer[i][1] += 0.1
            timer[i][2] = 0.1
            mutex.release()
            print timer[i][0], timer[i][3]
    except urllib2.HTTPError as e:
        code = e.code
        if code == 503:
            pass


if __name__ == '__main__':
    mutex = threading.Lock()
    # timer = [[sdk, start_time, wait_time, start_chunk_id]]
    for num in range(1):
        timer.append([num, 0, 0, 0])
    threading.Thread(target=fake_sdk).start()

# main function query memory conversion strategy effect

import threading
from multiprocessing import Process
import time
from config_loader import Loader
from faker import fake_sdk
from log import Log

loader = Loader()
config_info = loader.load_config_file()
sdks_get_file_dict = config_info['sdks_get_file_dict']
file_info = config_info['files_info']
start_chunk_id = config_info['start_chunk_id']
continue_requeste_interval = config_info['sdk_continue_requeste_interval']
threads = []
random_cri = []

# after the successful distribution of the proportion of waiting time
for i in continue_requeste_interval:
    for x in xrange(0, continue_requeste_interval[i]):
        random_cri.append(i)


def main_function(thread_num, process_num):
    t_pool = []
    log = Log('log', 'sdk_faker.log')
    file_size = 0
    ppc = 0
    file_id = ""
    for file_id, sdk_nums in sdks_get_file_dict.items():
        file_size = file_info[file_id]['file_size']
        ppc = file_info[file_id]['ppc']
    for num in range(thread_num):
        thread = threading.Thread(target=fake_sdk, args=(
            process_num,
            num,
            file_size,
            file_id,
            ppc,
            log,
            start_chunk_id
        ))
        thread.setDaemon(True)
        t_pool.append(thread)

    for t in t_pool:
        t.start()

    for t in t_pool:
        t.join()


if __name__ == '__main__':
    print time.time()
    process_num = 8
    thread_num = 93
    process_list = list()

    for i in range(process_num):
        p = Process(target=main_function, args=(thread_num, i))
        p.daemon = True
        p.start()
        process_list.append(p)

    for p in process_list:
        p.join()
    print time.time()

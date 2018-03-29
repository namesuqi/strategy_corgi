# Convert vod push monitor log
def read(log_file):
    with open(log_file) as f:
        info = f.read()
        info_splits = info.rstrip().split('\n')
        make_up = []
        for info_split in info_splits:
            change_symbol = []
            for info_item in info_split.split('\x1f'):
                change_symbol.append(info_item.replace('=', ':'))
            make_up.append(change_symbol)
        return make_up


def write(pending_list, target_file):
    with open(target_file, 'w') as f:
        for pending_info in pending_list:
            f.write(str(pending_info) + '\n')
        f.close()


if __name__ == '__main__':
    get_list = read('monitor.log')
    write(get_list, 'llll.log')

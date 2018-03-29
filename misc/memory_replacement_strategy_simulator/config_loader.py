# load conf.ini
import ConfigParser


class Loader(object):
    def __init__(self):
        self.loader = ConfigParser.ConfigParser()
        self.loader.read('conf.ini')

    def load_config_file(self):
        # push
        push_host = self.loader.get('push', 'push_host')
        headers_push = self.loader.get('push', 'headers_push')

        # sdk
        sdks_get_file_dict = self.loader.get('sdk', 'sdks_get_file_dict')
        sdk_continue_requeste_interval = self.loader.get(
            'sdk', 'sdk_continue_requeste_interval')
        sdk_re_request_interval = self.loader.get('sdk',
                                                  'sdk_re_request_interval')
        # chunk
        start_chunk_id = self.loader.get('chunk', 'start_chunk_id')
        chunks_per_query = self.loader.get('chunk', 'chunks_per_query')

        # cppc
        cppc = self.loader.get('cppc', 'cppc')

        # vod_push_file_on_disk
        files_info = self.loader.get('vod_push_file_on_disk', 'files_info')

        return {
            'start_chunk_id': eval(start_chunk_id),
            'chunks_per_query': eval(chunks_per_query),
            'cppc': eval(cppc),
            'push_host': push_host,
            'headers_push': headers_push,
            'sdks_get_file_dict': eval(sdks_get_file_dict),
            'sdk_continue_requeste_interval':
                eval(sdk_continue_requeste_interval),
            'sdk_re_request_interval': eval(sdk_re_request_interval),
            'files_info': eval(files_info)}

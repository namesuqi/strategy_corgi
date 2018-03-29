# coding=utf-8
# author: JinYiFan

import random

name = 'bond0'
livepush_version = '2.9.10'
receive = 2755416837
transmit = 9362935205
bandwidth = 4000
cpu_count = 24
cpu_load_1m = 1.960000
puff_thread_count = 4
supp_thread_count = 4
livepush_cpu_used_percentage = 0.000130
mem_total = 33651236864
mem_used = 19612463104

livepush_mem_used_percentage = ("%.6f" % ((mem_used * 1.0 / mem_total) * 0.01))

event_normal = ["supp_acl_close", "puff_acl_close"]
event_unnormal = ["supp_acl_close", "puff_acl_close", "supp_acl_open", "puff_acl_open"]
reason_normal = ["NA"]
reason_unnormal = ["mem_leak", "cpu_leak", "supp_overflow", "puff_overflow"]

print random.choice(event_normal)

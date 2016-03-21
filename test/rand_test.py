#!/usr/bin/env python
import time
from ddbpy.client import Send

dfe = ('127.0.0.1', 5555)
bucket = 'test'

with Send(dfe) as send:
    send.switch_streaming(bucket)
    while True:
        ts = int(time.time())
        value = "123.456"
        metric = "float"
        send.send_payload(metric, ts, value)
        time.sleep(1)
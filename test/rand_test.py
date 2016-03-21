#!/usr/bin/env python
import time
from ddbpy.client import Send

dfe = ('127.0.0.1', 5555)

with Send(dfe) as send:
    while True:
        ts = int(time.time())
        value = "123.456"
        metric = "float"
        send.send_payload(metric, ts, value)
        time.sleep(1)
#!/usr/bin/env python
import binascii
import socket
import struct
import dproto_tcp
import time


from dproto_hdr import LIST_BUCKETS, METRICS_SS, BUCKETS_SS, PACK_FMT, TCP_SS, \
    LIST_METRICS, STREAM_MODE, PAYLOAD, TIME_SIZE, FLUSH

remote = ('167.114.250.104', 5555)
tomasz = ('192.168.15.51', 5555)
local = ('127.0.0.1', 5555)



class API():

    def __init__(self, address):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(address)
        self.streaming_bucket = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def __del__(self):
        self.close()

    def close(self):
        if self.sock:
            print "closing socket"
            self.sock.close()
            self.sock = None

    def _send(self, packet):
        length = struct.pack(PACK_FMT[TCP_SS], len(packet))
        print binascii.hexlify(length + packet)
        self.sock.sendall(length + packet)

    def _recv(self):
        header = self.sock.recv(TCP_SS)
        length, = struct.unpack(PACK_FMT[TCP_SS], header)
        data = ''
        while len(data) < length:
            data += self.sock.recv(length)
        return data

    def list_buckets(self):
        self._send(LIST_BUCKETS)
        binary = self._recv()
        reply = dproto_tcp.decode_reply(binary, BUCKETS_SS)
        return dproto_tcp.decode_buckets(reply)

    def list_metrics(self, bucket):
        packet = dproto_tcp.encode_name(bucket)
        self._send(LIST_METRICS + packet)
        binary = self._recv()
        reply = dproto_tcp.decode_reply(binary, METRICS_SS)
        return dproto_tcp.decode_metrics(reply)

    def switch_streaming(self, bucket):
        if self.streaming_bucket:
            # TODO support switching bucket
            return

        delay = struct.pack("B", 5)
        pname = dproto_tcp.encode_name(bucket)
        self._send(STREAM_MODE + delay + pname)
        self.streaming_bucket = bucket

    def send_payload(self, metric, ts, value):
        if self.streaming_bucket is None:
            raise Exception("cannot send payload outside of stream mode")

        ptime = struct.pack(PACK_FMT[TIME_SIZE], ts)
        pmetric = dproto_tcp.encode_name(metric)
        pmetric_size = struct.pack(PACK_FMT[2], len(pmetric))

        pvalue = dproto_tcp.encode_metric_value(value)
        pvalue_size = struct.pack(PACK_FMT[4], len(pvalue))
        self._send(PAYLOAD + ptime + pmetric_size + pmetric + pvalue_size + pvalue)

    def flush(self):
        self._send(FLUSH)


with API(remote) as api:
    # res =  list_buckets()
    # res = api.list_metrics("dalmatinerdb")
    api.switch_streaming("dalmatinerdb")

    while True:
        ts = int(time.time())
        value = 10
        metric = "colin"
        api.send_payload(metric, ts, value)
        api.flush
        time.sleep(1)

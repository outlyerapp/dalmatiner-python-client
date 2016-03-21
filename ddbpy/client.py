#!/usr/bin/env python
import binascii
import socket
import struct
import dproto_tcp
from dproto_hdr import LIST_BUCKETS, METRICS_SS, BUCKETS_SS, PACK_FMT, TCP_SS, LIST_METRICS, STREAM_MODE, PAYLOAD, TIME_SIZE


class Send(object):
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
        self._raw_send(length + packet)

    def _raw_send(self, packet):
        print binascii.hexlify(packet)
        self.sock.sendall(packet)

    def send_payload(self, metric, ts, value):
        if self.streaming_bucket is None:
            raise Exception("cannot send payload outside of stream mode")

        ptime = struct.pack(PACK_FMT[TIME_SIZE], ts)
        pmetric = dproto_tcp.encode_name(metric)
        pmetric_size = struct.pack(PACK_FMT[2], len(pmetric))

        pvalue = dproto_tcp.encode_metric_value(value)
        pvalue_size = struct.pack(PACK_FMT[4], len(pvalue))
        self._raw_send(PAYLOAD + ptime + pmetric_size + pmetric + pvalue_size +
                       pvalue)

    def switch_streaming(self, bucket):
        if self.streaming_bucket:
            # TODO support switching bucket
            return
        delay = struct.pack("B", 5)
        pname = dproto_tcp.encode_name(bucket)
        self._send(STREAM_MODE + delay + pname)
        self.streaming_bucket = bucket


class Query(object):
    def __init__(self, address):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(address)
        self.streaming_bucket = None

    def _send(self, packet):
        length = struct.pack(PACK_FMT[TCP_SS], len(packet))
        self._raw_send(length + packet)

    def _raw_send(self, packet):
        print binascii.hexlify(packet)
        self.sock.sendall(packet)

    def _recv(self):
        header = self.sock.recv(TCP_SS)
        remaining, = struct.unpack(PACK_FMT[TCP_SS], header)
        msg = bytearray()
        while remaining > 0:
            chunk = self.sock.recv(remaining)
            msg.extend(chunk)
            remaining -= len(chunk)
        return msg

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

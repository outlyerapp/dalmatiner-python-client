import struct

from dproto_hdr import METRICS_SS, BUCKET_SS, PACK_FMT, METRIC_SS


def decode_buckets(binary, list=[]):
    return decode_list(binary, BUCKET_SS)


def decode_metrics(binary):
    return decode_list(binary, METRIC_SS)


def decode_list(binary, fmt, list=[]):
    if len(binary) <= fmt:
        return list

    length, = struct.unpack(PACK_FMT[fmt], binary[:fmt])
    payload = binary[fmt:fmt+length]
    # item, = struct.unpack('%ds' % length, payload)
    item = decode_metric(payload)
    list.append(item)
    return decode_list(binary[fmt+length:], fmt, list)



def decode_reply(binary, fmt):
    reply_size, = struct.unpack(PACK_FMT[fmt], binary[:fmt])
    reply_end = fmt + reply_size

    if len(binary) < reply_end:
        raise Exception("Corrupt response")

    return binary[fmt:reply_end]

def decode_metric(binary, components=[]):
    if len(binary) <= 1:
        return components

    length, = struct.unpack(PACK_FMT[1], binary[:1])
    name, = struct.unpack("%ds" % length, binary[1: length + 1])
    components.append(name)
    return decode_metric(binary[length + 1:])


def encode_name(name):
    length = len(name)
    plenth = struct.pack(PACK_FMT[1], length)
    pname = struct.pack("%ds" % length, name)
    return plenth + pname


def encode_metric_value(value):
    ptype = struct.pack(PACK_FMT[1], 1)
    pvalue = "\x00\x00\x00" + struct.pack(PACK_FMT[4], value)
    return ptype + pvalue

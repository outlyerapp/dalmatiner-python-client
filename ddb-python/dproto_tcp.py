import decimal
import dproto_hdr
import struct


def decode_buckets(binary, list=[]):
    return decode_list(binary, dproto_hdr.BUCKET_SS)


def decode_metrics(binary):
    return decode_list(binary, dproto_hdr.METRIC_SS)


def decode_list(binary, fmt, list=[]):
    if len(binary) <= fmt:
        return list

    length, = struct.unpack(dproto_hdr.PACK_FMT[fmt], binary[:fmt])
    payload = binary[fmt:fmt+length]

    item = decode_metric(payload)
    list.append(item)
    return decode_list(binary[fmt+length:], fmt, list)


def decode_reply(binary, fmt):
    reply_size, = struct.unpack(dproto_hdr.PACK_FMT[fmt], binary[:fmt])
    reply_end = fmt + reply_size

    if len(binary) < reply_end:
        raise Exception("Corrupt response")

    return binary[fmt:reply_end]


def decode_metric(binary, components=None):
    if len(binary) <= 1:
        return components

    if components is None:
        components = []

    length, = struct.unpack(dproto_hdr.PACK_FMT[1], binary[:1])
    name, = struct.unpack("%ds" % length, binary[1: length + 1])
    components.append(name)
    return decode_metric(binary[length + 1:], components)


def encode_name(name):
    length = len(name)
    plenth = struct.pack(dproto_hdr.PACK_FMT[1], length)
    pname = struct.pack("%ds" % length, name)
    return plenth + pname


def encode_metric_value(val_str):

    if not isinstance(val_str, basestring):
        """
        since data will be mostly coming in as a string and because
        its easier to do the float encoding, assume value is always a string
        """
        val_str = str(val_str)

    if is_float(val_str):
        return encode_float(val_str)
    else:
        return encode_int(val_str)


def encode_int(val_str):

    # pack the value in 8 bytes, then drop the least significant
    pvalue = struct.pack(">q", int(val_str))[1:]
    return dproto_hdr.POINT_INT + pvalue


def encode_float(val):
    """
    Note works best with string values, to prevent rounding issues with
    multiple conversions

    :param val:
    :return:
    """
    dec = decimal.Decimal(val)
    sign, digits, exponent, = dec.as_tuple()
    coefficient = idx = 0

    for d in digits:
        idx += 1

        if idx >= dproto_hdr.COEFFICIENT_LIMIT:
            exponent += 1
            continue

        if coefficient > 0:
            coefficient *= 10

        coefficient += d

    # pack the coefficient in 8 bytes, then drop the least significant
    pcoefficient = struct.pack(">q", coefficient)[2:]
    pexponent = struct.pack("b", exponent)

    return dproto_hdr.POINT_FLOAT + pexponent + pcoefficient










def is_float(value):
    return '.' in value


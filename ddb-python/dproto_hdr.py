COEFFICIENT_LIMIT = 14

POINT_NULL = '\x00'
POINT_INT = '\x01'
POINT_FLOAT = '\x02'

LIST_METRICS = '\x01'
LIST_BUCKETS = '\x03'
STREAM_MODE = '\x04'
PAYLOAD = '\x05'
FLUSH = '\x06'

# Payload sizes bytes
TCP_SS = 4
BUCKETS_SS = 8
BUCKET_SS = 2
METRICS_SS = 8
METRIC_SS = 2
TIME_SIZE = 8

PACK_FMT = {
    1: ">B",
    2: ">H",
    4: ">L",
    8: ">Q"

}
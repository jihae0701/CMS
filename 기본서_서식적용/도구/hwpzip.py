"""HWP 압축 스트림: raw deflate + [CRC32(4) + 원래 길이(4)] (한글이 이 꼬리를 검사함)"""
import zlib, struct
def compress(data):
    c = zlib.compressobj(9, zlib.DEFLATED, -15)
    return c.compress(data) + c.flush() + struct.pack('<II', zlib.crc32(data) & 0xffffffff, len(data) & 0xffffffff)
def check(raw):
    d = zlib.decompressobj(-15); out = d.decompress(raw)
    t = d.unused_data
    return d.eof and len(t) == 8 and struct.unpack('<II', t) == (zlib.crc32(out) & 0xffffffff, len(out) & 0xffffffff)

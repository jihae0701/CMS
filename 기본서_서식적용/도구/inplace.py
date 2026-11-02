"""원본 복합 파일 바이트를 그대로 두고 한 스트림(큰 스트림)의 내용만 같은 섹터 사슬 안에 다시 쓴다."""
import struct, olefile
ENDOFCHAIN, FREESECT = 0xFFFFFFFE, 0xFFFFFFFF

def replace_stream(src, dst, path, data):
    buf = bytearray(open(src, 'rb').read())
    ss = 1 << struct.unpack_from('<H', buf, 30)[0]
    assert ss == 512
    nfat, dir_start = struct.unpack_from('<II', buf, 44)[0], struct.unpack_from('<I', buf, 48)[0]
    difat_start, ndifat = struct.unpack_from('<II', buf, 68)
    fatsecs = list(struct.unpack_from('<109I', buf, 76))[:min(nfat, 109)]
    s = difat_start
    for _ in range(ndifat):
        ents = struct.unpack_from('<128I', buf, (s + 1) * ss)
        fatsecs += list(ents[:127]); s = ents[127]
    fatsecs = fatsecs[:nfat]
    def fat_get(i): return struct.unpack_from('<I', buf, (fatsecs[i // 128] + 1) * ss + (i % 128) * 4)[0]
    def fat_set(i, v): struct.pack_into('<I', buf, (fatsecs[i // 128] + 1) * ss + (i % 128) * 4, v)
    def chain(st):
        out = []
        while st not in (ENDOFCHAIN, FREESECT):
            out.append(st); st = fat_get(st)
        return out
    ole = olefile.OleFileIO(src)
    sid = ole._find(path); ole.close()
    dchain = chain(dir_start)
    eoff = (dchain[sid // 4] + 1) * ss + (sid % 4) * 128
    start, size = struct.unpack_from('<II', buf, eoff + 116)
    assert size >= 4096 and len(data) >= 4096
    ch = chain(start)
    need = (len(data) + ss - 1) // ss
    if need > len(ch):
        return False
    pad = data + b'\0' * (need * ss - len(data))
    for j in range(need):
        buf[(ch[j] + 1) * ss:(ch[j] + 2) * ss] = pad[j * ss:(j + 1) * ss]
    fat_set(ch[need - 1], ENDOFCHAIN)
    for s in ch[need:]:
        fat_set(s, FREESECT)
        buf[(s + 1) * ss:(s + 2) * ss] = b'\0' * ss
    struct.pack_into('<I', buf, eoff + 120, len(data))
    open(dst, 'wb').write(buf)
    return True

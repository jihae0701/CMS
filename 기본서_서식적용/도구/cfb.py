# Minimal Compound File Binary (OLE2, v3, 512-byte sectors) writer.
# Reads every storage/stream of an existing file with olefile and writes them back,
# letting chosen streams be replaced with data of any size.
import olefile, struct

ENDOFCHAIN, FREESECT, FATSECT, NOSTREAM = 0xFFFFFFFE, 0xFFFFFFFF, 0xFFFFFFFD, 0xFFFFFFFF
SS, MSS, CUTOFF = 512, 64, 4096


class Node:
    def __init__(s, name, kind, data=b'', clsid=b'\0' * 16, state=0):
        s.name, s.kind, s.data, s.clsid, s.state = name, kind, data, clsid, state
        s.kids = []   # Node list for storages
        s.left = s.right = s.child = NOSTREAM
        s.start, s.size = ENDOFCHAIN, 0


def read_tree(path):
    ole = olefile.OleFileIO(path)

    def build(de):
        n = Node(de.name, de.entry_type, b'', clsid_bytes(de.clsid), de.dwUserFlags)
        for k in de.kids:
            n.kids.append(build(k))
        return n

    root = build(ole.root)

    def fill(n, path):
        if n.kind == olefile.STGTY_STREAM:
            n.data = ole.openstream(path).read()
        for k in n.kids:
            fill(k, path + [k.name])
    for k in root.kids:
        fill(k, [k.name])
    ole.close()
    return root


def clsid_bytes(s):
    if not s:
        return b'\0' * 16
    import uuid
    return uuid.UUID(s).bytes_le


def cmpkey(n):
    return (len(n.name), n.name.upper())


def write(root, path):
    # flatten
    nodes = []

    def walk(n):
        nodes.append(n)
        for k in n.kids:
            walk(k)
    walk(root)
    for i, n in enumerate(nodes):
        n.idx = i
    # sibling trees (balanced BST)
    def bst(lst):
        if not lst:
            return NOSTREAM
        m = len(lst) // 2
        n = lst[m]
        n.left = bst(lst[:m])
        n.right = bst(lst[m + 1:])
        return n.idx
    for n in nodes:
        if n.kind in (olefile.STGTY_STORAGE, olefile.STGTY_ROOT):
            n.child = bst(sorted(n.kids, key=cmpkey))
    # mini stream
    mini = bytearray()
    minifat = []
    for n in nodes:
        if n.kind == olefile.STGTY_STREAM and len(n.data) < CUTOFF:
            n.size = len(n.data)
            if n.size == 0:
                n.start = ENDOFCHAIN
                continue
            cnt = (n.size + MSS - 1) // MSS
            n.start = len(minifat)
            for j in range(cnt):
                minifat.append(n.start + j + 1 if j < cnt - 1 else ENDOFCHAIN)
            mini += n.data + b'\0' * (cnt * MSS - n.size)
    # big streams: lay out sectors
    sectors = []          # list of bytes (512 each)
    fat = []

    def alloc(data):
        if not data:
            return ENDOFCHAIN
        cnt = (len(data) + SS - 1) // SS
        start = len(sectors)
        pad = data + b'\0' * (cnt * SS - len(data))
        for j in range(cnt):
            sectors.append(pad[j * SS:(j + 1) * SS])
            fat.append(start + j + 1 if j < cnt - 1 else ENDOFCHAIN)
        return start
    for n in nodes:
        if n.kind == olefile.STGTY_STREAM and len(n.data) >= CUTOFF:
            n.size = len(n.data)
            n.start = alloc(bytes(n.data))
    root.start = alloc(bytes(mini)) if mini else ENDOFCHAIN
    root.size = len(mini)
    mf = b''.join(struct.pack('<I', x) for x in minifat)
    if mf:
        mf += struct.pack('<I', FREESECT) * ((-len(minifat)) % (SS // 4))
    minifat_start = alloc(mf) if mf else ENDOFCHAIN
    nminifat = len(mf) // SS
    # directory
    ents = bytearray()
    for n in nodes:
        nm = n.name.encode('utf-16le')
        e = nm + b'\0\0'
        e = e + b'\0' * (64 - len(e))
        e += struct.pack('<HBB', len(nm) + 2, n.kind, 1)  # all black
        e += struct.pack('<III', n.left, n.right, n.child)
        e += n.clsid
        e += struct.pack('<I', n.state)
        e += b'\0' * 16  # times
        e += struct.pack('<III', n.start if (n.kind == olefile.STGTY_STREAM or n is root) else 0,
                         n.size if (n.kind == olefile.STGTY_STREAM or n is root) else 0, 0)
        ents += e
    while len(ents) % SS:
        ents += (b'\0' * 64 + struct.pack('<HBB', 0, 0, 0) + struct.pack('<III', NOSTREAM, NOSTREAM, NOSTREAM)
                 + b'\0' * 16 + b'\0' * 4 + b'\0' * 16 + b'\0' * 12)
    dir_start = alloc(bytes(ents))
    # FAT sectors (+DIFAT if needed)
    nsec = len(sectors)
    nfat = 1
    while True:
        ndifat = 0 if nfat <= 109 else (nfat - 109 + 126) // 127
        if (nsec + nfat + ndifat) <= nfat * 128:
            break
        nfat += 1
    fat_start = len(sectors)
    for j in range(nfat):
        fat.append(FATSECT)
        sectors.append(None)
    difat_start = len(sectors) if ndifat else ENDOFCHAIN
    for j in range(ndifat):
        fat.append(0xFFFFFFFC)
        sectors.append(None)
    fat += [FREESECT] * (nfat * 128 - len(fat))
    for j in range(nfat):
        sectors[fat_start + j] = b''.join(struct.pack('<I', x) for x in fat[j * 128:(j + 1) * 128])
    fatlocs = list(range(fat_start, fat_start + nfat))
    for j in range(ndifat):
        chunk = fatlocs[109 + j * 127:109 + (j + 1) * 127]
        chunk += [FREESECT] * (127 - len(chunk))
        nxt = difat_start + j + 1 if j < ndifat - 1 else ENDOFCHAIN
        sectors[difat_start + j] = b''.join(struct.pack('<I', x) for x in chunk) + struct.pack('<I', nxt)
    hdr = bytearray(b'\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1' + b'\0' * 16)
    hdr += struct.pack('<HHHHH', 0x3E, 3, 0xFFFE, 9, 6)
    hdr += b'\0' * 6
    hdr += struct.pack('<IIIIIIIII', 0, nfat, dir_start, 0, CUTOFF, minifat_start, nminifat, difat_start, ndifat)
    head = fatlocs[:109] + [FREESECT] * (109 - min(109, nfat))
    hdr += b''.join(struct.pack('<I', x) for x in head)
    assert len(hdr) == 512
    with open(path, 'wb') as f:
        f.write(hdr)
        for s in sectors:
            f.write(s)


def find(root, path):
    n = root
    for p in path.split('/'):
        n = next(k for k in n.kids if k.name == p)
    return n

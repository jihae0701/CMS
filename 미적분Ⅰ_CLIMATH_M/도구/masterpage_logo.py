import sys, zipfile, shutil, re
src = sys.argv[1]; logo = zipfile.ZipFile(src).read('BinData/image1.png')
for dst in sys.argv[2:]:
    zi = zipfile.ZipFile(dst); items = [(i, zi.read(i.filename)) for i in zi.infolist()]; zi.close()
    sec = dict((i.filename, d) for i, d in items)['Contents/section0.xml'].decode()
    assert 'binaryItemIDRef="image1"' not in sec, dst
    tmp = dst + '.tmp'
    with zipfile.ZipFile(tmp, 'w') as zo:
        for info, data in items:
            if info.filename == 'BinData/image1.png': data = logo
            zo.writestr(info, data, compress_type=info.compress_type)
    shutil.move(tmp, dst); print('로고 바꿈', dst.split('/')[-2], dst.split('/')[-1])

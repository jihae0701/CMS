import sys, zipfile, shutil, re, html
path = sys.argv[1]
z = zipfile.ZipFile(path); items = [(i, z.read(i.filename)) for i in z.infolist()]; z.close()
with zipfile.ZipFile(path + '.tmp', 'w') as zo:
    for info, data in items:
        if info.filename == 'Contents/section0.xml':
            t = data.decode('utf-8')
            t, n = re.subn(r'&lt;(hp:(?:lineBreak|tab)\b[^&]*?/)&gt;', lambda m: '<' + html.unescape(m.group(1)) + '>', t)
            print('복구', n)
            data = t.encode('utf-8')
        zo.writestr(info, data, compress_type=info.compress_type)
shutil.move(path + '.tmp', path)

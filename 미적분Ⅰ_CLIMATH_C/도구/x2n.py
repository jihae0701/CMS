import sys, html
sys.path.insert(0, '.')
import hwpxedit as H
P = sys.argv[1]; x = H.load(P); n = [0]
def f(m):
    s = html.unescape(m.group(2)); t = s.replace('x^2n-1', 'x^{2n-1}').replace('x^2n-2', 'x^{2n-2}').replace('x^2n', 'x^{2n}')
    if t != s: n[0] += 1
    return m.group(1) + html.escape(t, quote=False) + m.group(3)
y = H.SC.sub(f, x)
if y != x: H.save(P, y)
print(P, 'x^2n', n[0])

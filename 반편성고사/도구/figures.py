# 모의고사 그림 스타일(검정 실선, 화살표 좌표축, Computer Modern 글꼴)로 변형 문항 그림 생성
import sys, os, shutil
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Circle, Polygon

OUT = sys.argv[1]
SRC = sys.argv[2]  # 원본 그림 폴더(exams)
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"mathtext.fontset": "cm", "font.family": "serif", "font.serif": ["DejaVu Serif"]})
LW = 1.6
FS = 15

def axes(ax, xmin, xmax, ymin, ymax, ox=0, oy=0, olabel=True):
    ax.annotate("", xy=(xmax, oy), xytext=(xmin, oy),
                arrowprops=dict(arrowstyle="-|>,head_length=0.6,head_width=0.25", lw=LW, color="k"))
    ax.annotate("", xy=(ox, ymax), xytext=(ox, ymin),
                arrowprops=dict(arrowstyle="-|>,head_length=0.6,head_width=0.25", lw=LW, color="k"))
    ax.text(xmax, oy - (ymax - ymin) * 0.035, r"$x$", fontsize=FS, ha="center", va="top")
    ax.text(ox - (xmax - xmin) * 0.035, ymax, r"$y$", fontsize=FS, ha="right", va="center")
    if olabel:
        ax.text(ox - (xmax - xmin) * 0.02, oy - (ymax - ymin) * 0.02, r"$\mathrm{O}$", fontsize=FS, ha="right", va="top")

def finish(fig, ax, name, xlim, ylim):
    ax.set_xlim(*xlim); ax.set_ylim(*ylim)
    ax.set_aspect("equal"); ax.axis("off")
    fig.savefig(os.path.join(OUT, name), dpi=220, bbox_inches="tight", pad_inches=0.05, facecolor="white")
    plt.close(fig)

def lab(ax, x, y, s, **kw):
    kw.setdefault("fontsize", FS)
    ax.text(x, y, s, **kw)

# 1) 공수2 2번: 대응 그림 f(1)=4, f(2)=1, f(3)=5, f(4)=2, f(5)=3
fig, ax = plt.subplots(figsize=(4.0, 3.1))
for cx in (0, 5):
    ax.add_patch(Ellipse((cx, 2.55), 2.4, 5.5, fill=False, lw=LW))
    lab(ax, cx, 5.75, r"$X$", ha="center", va="center", fontsize=FS + 1)
ax.annotate("", xy=(3.5, 5.55), xytext=(1.5, 5.55), arrowprops=dict(arrowstyle="-|>", lw=LW, color="k"))
lab(ax, 2.5, 5.75, r"$f$", ha="center", va="bottom")
ys = {i: 4.6 - (i - 1) * 1.0 for i in range(1, 6)}
for i in range(1, 6):
    lab(ax, -0.1, ys[i], f"${i}$", ha="center", va="center")
    lab(ax, 5.1, ys[i], f"${i}$", ha="center", va="center")
for s, d in {1: 4, 2: 1, 3: 5, 4: 2, 5: 3}.items():
    ax.annotate("", xy=(4.6, ys[d]), xytext=(0.35, ys[s]),
                arrowprops=dict(arrowstyle="-|>,head_length=0.5,head_width=0.2", lw=1.2, color="k", shrinkA=0, shrinkB=2))
finish(fig, ax, "mapping.png", (-1.5, 6.5), (-0.4, 6.2))

# 2) 공수2 9번: f(x)=sqrt(2x), A(2,2), B(18,6), C, D (모양을 위해 x축 축척 조정)
fig, ax = plt.subplots(figsize=(4.6, 3.0))
sx = 0.35  # x 방향 축척
X = np.linspace(0, 22, 400)
axes(ax, -1.2, 22 * sx + 0.6, -1.2, 7.4)
ax.plot(X * sx, np.sqrt(2 * X), "k", lw=LW)
A = (2 * sx, 2); B = (18 * sx, 6)
ax.plot([A[0], B[0]], [A[1], B[1]], "k", lw=LW)
for P in (A, B):
    ax.plot([P[0], P[0]], [0, P[1]], "k", lw=LW)
    ax.plot([P[0], P[0] + 0.22, P[0] + 0.22], [0.22, 0.22, 0], "k", lw=0.9)
lab(ax, A[0] - 0.1, A[1] + 0.25, r"$\mathrm{A}$", ha="center", va="bottom")
lab(ax, B[0], B[1] + 0.3, r"$\mathrm{B}$", ha="center", va="bottom")
lab(ax, A[0], -0.3, r"$\mathrm{C}$", ha="center", va="top")
lab(ax, B[0], -0.3, r"$\mathrm{D}$", ha="center", va="top")
lab(ax, 2.3, 6.0, r"$f\,(x)\!=\!\sqrt{2x}$", ha="center", va="bottom")
finish(fig, ax, "sqrt.png", (-1.4, 22 * sx + 1.0), (-1.4, 7.8))

# 3) 공수2 11번: 원 (x-10)^2+(y-6)^2=5, A(1,0), y=x, Q, P
fig, ax = plt.subplots(figsize=(4.2, 3.4))
axes(ax, -1.2, 14.0, -1.5, 11.5, olabel=False)
lab(ax, -0.25, -0.3, r"$\mathrm{O}$", ha="right", va="top")
ax.plot([-0.8, 10.8], [-0.8, 10.8], "k", lw=LW)
lab(ax, 10.8, 11.0, r"$y\!=\!x$", ha="center", va="bottom")
r = 5 ** 0.5
ax.add_patch(Circle((10, 6), r, fill=False, lw=LW))
lab(ax, 10 + r * 0.8, 6 + r * 0.8, r"$C$", ha="left", va="bottom")
Aq = (2.6, 0); Q = (5.4, 5.4)
P = (10 - r * 0.92, 6 + r * 0.39)
ax.plot([Aq[0], Q[0]], [Aq[1], Q[1]], "k", lw=LW)
ax.plot([Q[0], P[0]], [Q[1], P[1]], "k", lw=LW)
lab(ax, Aq[0], -0.35, r"$\mathrm{A}$", ha="center", va="top")
lab(ax, Q[0] - 0.3, Q[1] + 0.2, r"$\mathrm{Q}$", ha="right", va="bottom")
lab(ax, P[0] - 0.1, P[1] + 0.3, r"$\mathrm{P}$", ha="right", va="bottom")
finish(fig, ax, "reflect.png", (-1.5, 14.5), (-1.8, 12))

# 4) 공수2 13번: f=3sqrt(x), g=x^2/9, A(9,9), P(4,4), B(16/9,4), C(6,4)
fig, ax = plt.subplots(figsize=(4.0, 3.6))
axes(ax, -1.5, 13.2, -1.8, 12.2)
X = np.linspace(0, 11.2, 400)
ax.plot(X, 3 * np.sqrt(X), "k", lw=LW)
X2 = np.linspace(0, 10.2, 400)
ax.plot(X2, X2 ** 2 / 9, "k", lw=LW)
A = (9, 9); P = (4, 4); B = (16 / 9, 4); Cc = (6, 4)
ax.add_patch(Polygon([A, B, Cc], closed=True, facecolor="#e0e0e0", edgecolor="k", lw=LW))
ax.plot([0, A[0]], [0, A[1]], "k", lw=1.2)
ax.plot([-0.8, 12], [4, 4], "k", lw=LW)
lab(ax, A[0] - 0.3, A[1] + 0.3, r"$\mathrm{A}$", ha="right", va="bottom")
lab(ax, B[0] + 0.05, 3.7, r"$\mathrm{B}$", ha="center", va="top")
lab(ax, P[0] + 0.15, 3.7, r"$\mathrm{P}$", ha="center", va="top")
lab(ax, Cc[0] + 0.3, 3.7, r"$\mathrm{C}$", ha="center", va="top")
lab(ax, 11.3, 10.3, r"$y\!=\!f\,(x)$", ha="left", va="center")
lab(ax, 10.0, 11.9, r"$y\!=\!g\,(x)$", ha="center", va="bottom")
finish(fig, ax, "twocurve.png", (-1.8, 14), (-2.0, 12.8))

# 5) 공수2 14번: 원 (x-4)^2+(y-2)^2=4, y=x/7, A, H, B
fig, ax = plt.subplots(figsize=(4.2, 3.2))
axes(ax, -1.2, 8.6, -1.4, 5.6)
ax.add_patch(Circle((4, 2), 2, fill=False, lw=LW))
m = 1 / 7
X = np.linspace(0, 7.6, 10)
ax.plot(X, m * X, "k", lw=LW)
lab(ax, 7.6, m * 7.6 + 0.15, r"$y\!=\!mx$", ha="center", va="bottom")
A = np.array([4, 2]); u = np.array([1, m]) / np.hypot(1, m)
H = u * (A @ u)
ax.plot(*A, "ko", ms=5)
ax.plot([A[0], H[0]], [A[1], H[1]], "k", lw=LW)
n = np.array([-u[1], u[0]]); s = 0.22
sq = [H + u * s, H + u * s + n * s, H + n * s]
ax.plot([q[0] for q in sq], [q[1] for q in sq], "k", lw=0.9)
tB = A @ u - np.sqrt(4 - (np.linalg.norm(A - H)) ** 2)
Bp = u * tB
lab(ax, A[0], A[1] + 0.2, r"$\mathrm{A}$", ha="center", va="bottom")
lab(ax, H[0] + 0.05, H[1] - 0.2, r"$\mathrm{H}$", ha="center", va="top")
lab(ax, Bp[0] - 0.1, Bp[1] + 0.15, r"$\mathrm{B}$", ha="center", va="bottom")
lab(ax, 5.6, 3.75, r"$C$", ha="left", va="bottom")
finish(fig, ax, "circleline.png", (-1.5, 9), (-1.7, 6))

# 6) 공수2 14번: 두 직선 y=3x, y=x/3에 접하는 원(중심 A(5,5)), 접점 P(2,6), Q(6,2), 직선 PQ와 x축의 교점 R(8,0)
fig, ax = plt.subplots(figsize=(4.0, 3.9))
axes(ax, -1.0, 10.6, -1.0, 10.2)
ax.add_patch(Circle((5, 5), np.sqrt(10), fill=False, lw=LW))
X = np.linspace(0, 3.2, 10)
ax.plot(X, 3 * X, "k", lw=LW)
X = np.linspace(0, 10.2, 10)
ax.plot(X, X / 3, "k", lw=LW)
ax.plot([1.3, 8.45], [6.7, -0.45], "k", lw=LW)
for (px, py) in ((5, 5), (2, 6), (6, 2), (8, 0)):
    ax.plot(px, py, "ko", ms=4.5)
lab(ax, 5.15, 5.15, r"$\mathrm{A}$", ha="left", va="bottom")
lab(ax, 1.55, 5.75, r"$\mathrm{P}$", ha="right", va="top")
lab(ax, 6.0, 1.6, r"$\mathrm{Q}$", ha="center", va="top")
lab(ax, 8.25, 0.15, r"$\mathrm{R}$", ha="left", va="bottom")
lab(ax, 3.35, 9.6, r"$l_1$", ha="left", va="center")
lab(ax, 10.25, 3.75, r"$l_2$", ha="left", va="center")
finish(fig, ax, "tangent2.png", (-1.4, 11.2), (-1.4, 10.6))

# 원본 그림 재사용(객실 번호·좌석 번호 배치가 같음)
shutil.copy(os.path.join(SRC, "img2025", "8.png"), os.path.join(OUT, "room.png"))
shutil.copy(os.path.join(SRC, "img2026", "17.png"), os.path.join(OUT, "chair.png"))
print(sorted(os.listdir(OUT)))

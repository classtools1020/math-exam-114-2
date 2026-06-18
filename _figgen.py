# -*- coding: utf-8 -*-
"""考卷幾何圖批次產生器 — 配合特教生，圖大、字大、標示清楚。"""
import os, math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Arc, FancyBboxPatch, Circle, Rectangle
from matplotlib import font_manager

plt.rcParams['font.family'] = 'Microsoft JhengHei'
plt.rcParams['axes.unicode_minus'] = False

OUT = os.path.join(os.path.dirname(__file__), '_figs')
os.makedirs(OUT, exist_ok=True)

# 配色（延續現有教學卡風格）
FILL   = '#dceafa'   # 淺藍填充
EDGE   = '#2e6da4'   # 深藍邊
DIAG   = '#e8973a'   # 橘色對角線（虛線）
GREEN  = '#27ae60'
PURPLE = '#8e44ad'
RED    = '#e74c3c'
TXT    = '#1f3a52'
GRAY   = '#888888'

def _new(w=3.4, h=2.6):
    fig, ax = plt.subplots(figsize=(w, h))
    ax.set_aspect('equal'); ax.axis('off')
    return fig, ax

def _save(fig, name):
    p = os.path.join(OUT, name)
    fig.savefig(p, dpi=170, bbox_inches='tight', pad_inches=0.12,
                facecolor='white')
    plt.close(fig)
    return p

def _tick(ax, p, q, kind=1, color=GREEN):
    """在線段 pq 中點畫等邊記號。kind=1 單槓, 2 雙槓。"""
    mx, my = (p[0]+q[0])/2, (p[1]+q[1])/2
    dx, dy = q[0]-p[0], q[1]-p[1]
    L = math.hypot(dx, dy); ux, uy = dx/L, dy/L
    nx, ny = -uy, ux  # 法線
    s = 0.10
    offs = [0] if kind == 1 else [-0.045, 0.045]
    for o in offs:
        cx, cy = mx+ux*o*L, my+uy*o*L
        ax.plot([cx-nx*s, cx+nx*s], [cy-ny*s, cy+ny*s],
                color=color, lw=2, zorder=5)

def _angle_arc(ax, vertex, p1, p2, label=None, color=RED, r=0.5, lw=2.2):
    a1 = math.degrees(math.atan2(p1[1]-vertex[1], p1[0]-vertex[0]))
    a2 = math.degrees(math.atan2(p2[1]-vertex[1], p2[0]-vertex[0]))
    # 取較小夾角方向
    d = (a2 - a1) % 360
    if d > 180:
        a1, a2 = a2, a1
    ax.add_patch(Arc(vertex, 2*r, 2*r, angle=0, theta1=min(a1, a2),
                     theta2=max(a1, a2), color=color, lw=lw, zorder=6))
    if label:
        mid = math.radians((min(a1, a2)+max(a1, a2))/2)
        lr = r + 0.34
        ax.text(vertex[0]+lr*math.cos(mid), vertex[1]+lr*math.sin(mid),
                label, color=color, fontsize=13, fontweight='bold',
                ha='center', va='center', zorder=7)

def _vlabel(ax, p, txt, dx, dy):
    ax.text(p[0]+dx, p[1]+dy, txt, fontsize=15, fontweight='bold',
            color=TXT, ha='center', va='center', zorder=8)

def _slabel(ax, p, q, txt, off=0.30, color=EDGE):
    mx, my = (p[0]+q[0])/2, (p[1]+q[1])/2
    dx, dy = q[0]-p[0], q[1]-p[1]
    L = math.hypot(dx, dy); nx, ny = -dy/L, dx/L
    ax.text(mx+nx*off, my+ny*off, txt, fontsize=13, color=color,
            ha='center', va='center', fontweight='bold', zorder=8)

def _title(ax, txt, x, y):
    ax.text(x, y, txt, fontsize=13, color=TXT, ha='center',
            va='center', fontweight='bold')

# ---------------------------------------------------------------------------
# 四邊形：A 左上, B 左下, C 右下, D 右上（配合現有 image5）
# 用一點傾斜畫出「平行四邊形」感
def quad(name, kind='para', side_labels=None, angle_at=None,
         diagonals=False, O_label=False, ticks=None, equal_marks=None,
         caption=None, right_angles=None, diag_labels=None):
    fig, ax = _new(3.4, 2.7)
    if kind == 'para':
        A, B, C, D = (0.55, 2.0), (0.0, 0.0), (2.4, 0.0), (2.95, 2.0)
    elif kind == 'rhombus':
        A, B, C, D = (1.2, 2.05), (0.1, 0.95), (1.2, -0.15), (2.3, 0.95)
    elif kind == 'rect':
        A, B, C, D = (0.1, 1.7), (0.1, 0.0), (2.9, 0.0), (2.9, 1.7)
    elif kind == 'square':
        A, B, C, D = (0.2, 2.0), (0.2, 0.0), (2.2, 0.0), (2.2, 2.0)
    elif kind == 'kite':
        A, B, C, D = (1.2, 2.2), (0.15, 1.1), (1.2, -0.45), (2.25, 1.1)
    elif kind == 'trap':  # 等腰梯形 AB//CD：A左上 B右上 C右下 D左下
        A, B, C, D = (0.7, 1.7), (2.1, 1.7), (2.8, 0.0), (0.0, 0.0)
    pts = [A, B, C, D]
    ax.add_patch(Polygon(pts, closed=True, facecolor=FILL,
                         edgecolor=EDGE, lw=2.6, zorder=2))
    # 頂點標籤（往外推）
    cen = (sum(p[0] for p in pts)/4, sum(p[1] for p in pts)/4)
    for p, nm in zip(pts, ['A', 'B', 'C', 'D']):
        ddx, ddy = p[0]-cen[0], p[1]-cen[1]
        L = math.hypot(ddx, ddy)
        _vlabel(ax, p, nm, ddx/L*0.34, ddy/L*0.34)
    names = {'A': A, 'B': B, 'C': C, 'D': D}
    # 邊長標籤 side_labels: dict like {'AB':'5'}
    if side_labels:
        for k, v in side_labels.items():
            _slabel(ax, names[k[0]], names[k[1]], v)
    # 等邊記號 ticks: list of (edge, kind, color)
    if ticks:
        for edge, knd, col in ticks:
            _tick(ax, names[edge[0]], names[edge[1]], knd, col)
    if diagonals:
        ax.plot([A[0], C[0]], [A[1], C[1]], '--', color=DIAG, lw=2, zorder=3)
        ax.plot([B[0], D[0]], [B[1], D[1]], '--', color=DIAG, lw=2, zorder=3)
        if O_label:
            ax.add_patch(Circle(cen, 0.06, color=RED, zorder=6))
            _vlabel(ax, cen, 'O', 0.22, 0.18)
        if diag_labels:  # 半對角線 {'AO':'6'} 標中點；整條 {'AC':'8'} 放近頂點 1/3 處避開 O
            for k, v in diag_labels.items():
                p = names[k[0]]
                if k[1] == 'O':
                    _slabel(ax, p, cen, v, off=0.24, color='#b9690f')
                else:
                    q = names[k[1]]
                    t = 0.30
                    px, py = p[0]+(q[0]-p[0])*t, p[1]+(q[1]-p[1])*t
                    dx, dy = q[0]-p[0], q[1]-p[1]; L = math.hypot(dx, dy)
                    nx, ny = -dy/L, dx/L
                    ax.text(px+nx*0.27, py+ny*0.27, v, fontsize=13,
                            color='#b9690f', ha='center', va='center',
                            fontweight='bold', zorder=8)
    if angle_at:  # dict {'A':'70°'}
        for v, lab in angle_at.items():
            P = names[v]
            order = ['A', 'B', 'C', 'D']
            i = order.index(v)
            nb1 = names[order[(i+1) % 4]]
            nb2 = names[order[(i-1) % 4]]
            _angle_arc(ax, P, nb1, nb2, lab, color=RED, r=0.42)
    if right_angles:
        for v in right_angles:
            P = names[v]; order = ['A', 'B', 'C', 'D']; i = order.index(v)
            nb1 = names[order[(i+1) % 4]]; nb2 = names[order[(i-1) % 4]]
            u1 = ((nb1[0]-P[0]), (nb1[1]-P[1])); l1 = math.hypot(*u1)
            u2 = ((nb2[0]-P[0]), (nb2[1]-P[1])); l2 = math.hypot(*u2)
            s = 0.22
            c1 = (P[0]+u1[0]/l1*s, P[1]+u1[1]/l1*s)
            c2 = (P[0]+u2[0]/l2*s, P[1]+u2[1]/l2*s)
            c3 = (c1[0]+c2[0]-P[0], c1[1]+c2[1]-P[1])
            ax.plot([c1[0], c3[0], c2[0]], [c1[1], c3[1], c2[1]],
                    color=EDGE, lw=1.4, zorder=6)
    ax.relim(); ax.autoscale_view()
    if caption:
        xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
        cx = (min(xs)+max(xs))/2; my = min(ys)
        ax.text(cx, my-0.78, caption, fontsize=11, color=GRAY,
                ha='center', va='top')
        ax.set_ylim(my-1.15, max(ys)+0.55)
        ax.set_xlim(min(xs)-0.75, max(xs)+0.75)
    return _save(fig, name)

# ---------------------------------------------------------------------------
def triangle(name, labels=('A', 'B', 'C'), sides=None, lengths=None,
             caption=None):
    """sides: dict {'AB':'5'} 邊長文字; lengths:(a,b,c) 用於決定形狀(BC,CA,AB)。"""
    fig, ax = _new(3.2, 2.5)
    if lengths and _valid(*lengths):
        a, b, c = lengths  # a=BC, b=CA, c=AB
        # B=(0,0), C=(a,0), A from b,c
        ax_ = (c**2 + a**2 - b**2) / (2*a)
        ay = math.sqrt(max(c**2 - ax_**2, 0.01))
        B, C, A = (0, 0), (a, 0), (ax_, ay)
        sc = 2.6 / max(a, ay, 1)
        B = (B[0]*sc, B[1]*sc); C = (C[0]*sc, C[1]*sc); A = (A[0]*sc, A[1]*sc)
    else:
        A, B, C = (1.3, 2.2), (0.0, 0.0), (2.8, 0.0)
    pts = [A, B, C]
    ax.add_patch(Polygon(pts, closed=True, facecolor=FILL, edgecolor=EDGE,
                         lw=2.6, zorder=2))
    cen = (sum(p[0] for p in pts)/3, sum(p[1] for p in pts)/3)
    for p, nm in zip(pts, labels):
        ddx, ddy = p[0]-cen[0], p[1]-cen[1]; L = math.hypot(ddx, ddy)
        _vlabel(ax, p, nm, ddx/L*0.3, ddy/L*0.3)
    nm = {labels[0]: A, labels[1]: B, labels[2]: C}
    if sides:
        for k, v in sides.items():
            _slabel(ax, nm[k[0]], nm[k[1]], v, off=0.28)
    ax.relim(); ax.autoscale_view()
    if caption:
        xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
        cx = (min(xs)+max(xs))/2; my = min(ys)
        ax.text(cx, my-0.62, caption, fontsize=11, color=GRAY,
                ha='center', va='top')
        ax.set_ylim(my-1.0, max(ys)+0.5)
        ax.set_xlim(min(xs)-0.7, max(xs)+0.7)
    return _save(fig, name)

def _valid(a, b, c):
    try:
        a, b, c = float(a), float(b), float(c)
    except Exception:
        return False
    return a+b > c and a+c > b and b+c > a

# ---------------------------------------------------------------------------
def parallel_lines(name, marked=None, l1=r'$L_1$', l2=r'$L_2$',
                   show_numbers=False, caption=None, tname='L', note=None):
    """兩平行線 + 截線。marked: list of (pos, text, color)
       pos in {'tl1','tr1','bl1','br1','tl2','tr2','bl2','br2'} 八個角位置。"""
    fig, ax = _new(3.6, 2.7)
    y1, y2 = 1.9, 0.4
    ax.plot([-0.2, 3.4], [y1, y1], color=EDGE, lw=2.4, zorder=2)
    ax.plot([-0.2, 3.4], [y2, y2], color=EDGE, lw=2.4, zorder=2)
    ax.text(3.5, y1, l1, color=EDGE, fontsize=12, va='center', fontweight='bold')
    ax.text(3.5, y2, l2, color=EDGE, fontsize=12, va='center', fontweight='bold')
    # 截線（斜）
    slope = 1.7
    def xat(y, x0):
        return x0 + (y - 1.15) / slope
    x0 = 1.5
    xtop, xbot = xat(2.6, x0), xat(-0.25, x0)
    ax.plot([xtop, xbot], [2.6, -0.25], color=RED, lw=2.4, zorder=3)
    ax.text(xtop-0.05, 2.72, tname, color=RED, fontsize=12, fontweight='bold')
    ix1 = (xat(y1, x0), y1); ix2 = (xat(y2, x0), y2)
    note_txt = note if note else r'$L_1 /\!/ L_2$'
    ax.text(0.0, 1.12, note_txt, color=EDGE, fontsize=12, fontweight='bold')
    # 八角位置
    def angpos(ix, where):
        ox = 0.32 if 'r' in where else -0.32
        oy = 0.28 if 't' in where else -0.28
        return (ix[0]+ox, ix[1]+oy)
    if show_numbers:
        m = [('tr1', '1'), ('tl1', '2'), ('bl1', '3'), ('br1', '4'),
             ('tr2', '5'), ('tl2', '6'), ('bl2', '7'), ('br2', '8')]
        for pos, t in m:
            ix = ix1 if pos.endswith('1') else ix2
            p = angpos(ix, pos)
            ax.text(p[0], p[1], t, fontsize=12, fontweight='bold',
                    color='#c0392b', ha='center', va='center')
    if marked:
        for pos, t, col in marked:
            ix = ix1 if pos.endswith('1') else ix2
            p = angpos(ix, pos)
            ax.text(p[0], p[1], t, fontsize=13, fontweight='bold',
                    color=col, ha='center', va='center')
    ax.set_xlim(-0.4, 4.0); ax.set_ylim(-0.45, 2.95)
    if caption:
        ax.text(1.6, -0.55, caption, fontsize=11, color=GRAY, ha='center')
        ax.set_ylim(-0.8, 2.95)
    return _save(fig, name)

# ---------------------------------------------------------------------------
def sticks(name, groups, caption=None):
    """groups: list of (title, [a,b,c])。每組畫「兩短邊相加」對比「最長邊」上下兩條。"""
    n = len(groups)
    fig, ax = _new(4.0, 1.25*n+0.7)
    allmax = max(sum(sorted(g[1])[:2]) if False else max(g[1]) for g in groups)
    allmax = max(max(g[1]) for g in groups + [('',[sum(sorted(g[1])[:2]) for g in groups])])
    allmax = max([max(g[1]) for g in groups] + [sum(sorted(g[1])[:2]) for g in groups])
    SCALE = 2.7 / allmax
    rowh = 1.25
    y = n * rowh
    BLUE, GREEN_, ORANGE = '#2e6da4', '#27ae60', '#e8973a'
    for title, lens in groups:
        s1, s2 = sorted(lens)[:2]
        longest = max(lens)
        can = (s1 + s2) > longest
        x0 = 0.7
        # 上條：兩短邊相加
        w1, w2 = s1*SCALE, s2*SCALE
        ax.add_patch(Rectangle((x0, y-0.14), w1, 0.30, facecolor=BLUE,
                     edgecolor='white', lw=1.2))
        ax.text(x0+w1/2, y, str(s1), color='white', fontsize=11,
                fontweight='bold', ha='center', va='center')
        ax.add_patch(Rectangle((x0+w1, y-0.14), w2, 0.30, facecolor=GREEN_,
                     edgecolor='white', lw=1.2))
        ax.text(x0+w1+w2/2, y, str(s2), color='white', fontsize=11,
                fontweight='bold', ha='center', va='center')
        ax.text(x0-0.12, y, '兩短邊', fontsize=9.5, color=TXT,
                ha='right', va='center')
        # 下條：最長邊
        yl = y - 0.46
        wl = longest*SCALE
        ax.add_patch(Rectangle((x0, yl-0.14), wl, 0.30, facecolor=ORANGE,
                     edgecolor='white', lw=1.2))
        ax.text(x0+wl/2, yl, str(longest), color='white', fontsize=11,
                fontweight='bold', ha='center', va='center')
        ax.text(x0-0.12, yl, '最長邊', fontsize=9.5, color=TXT,
                ha='right', va='center')
        # 群組標題 + 判斷虛線
        ax.text(x0-0.12, (y+yl)/2+0.42, title, fontsize=12, fontweight='bold',
                color=TXT, ha='left', va='center')
        edge = max(x0+w1+w2, x0+wl)
        ax.plot([x0, x0], [yl-0.2, y+0.2], color=GRAY, lw=0.8, ls=':')
        y -= rowh
    ax.set_xlim(-0.2, 3.7); ax.set_ylim(0.0, n*rowh+0.55)
    if caption:
        ax.text(1.7, 0.15, caption, fontsize=10, color=GRAY, ha='center')
    return _save(fig, name)


# ---------------------------------------------------------------------------
def _mini_shape(ax, cx, cy, kind, s=0.6, col=EDGE):
    """在 (cx,cy) 畫一個迷你四邊形。"""
    if kind == 'rect':
        pts = [(-1.0, 0.62), (1.0, 0.62), (1.0, -0.62), (-1.0, -0.62)]
    elif kind == 'square':
        pts = [(-0.7, 0.7), (0.7, 0.7), (0.7, -0.7), (-0.7, -0.7)]
    elif kind == 'rhombus':
        pts = [(0, 0.85), (0.75, 0), (0, -0.85), (-0.75, 0)]
    elif kind == 'kite':
        pts = [(0, 0.9), (0.6, 0.2), (0, -0.85), (-0.6, 0.2)]
    elif kind == 'trap':
        pts = [(-0.5, 0.6), (0.5, 0.6), (0.9, -0.6), (-0.9, -0.6)]
    elif kind == 'para':
        pts = [(-0.6, 0.6), (1.0, 0.6), (0.6, -0.6), (-1.0, -0.6)]
    pts = [(cx+x*s, cy+y*s) for x, y in pts]
    ax.add_patch(Polygon(pts, closed=True, facecolor=FILL, edgecolor=col,
                         lw=2.4, zorder=2))

def objects(name, items, caption=None):
    """items: list of (物品名,)。橫列迷你物品卡（只畫圖，不洩漏答案）。"""
    n = len(items)
    fig, ax = _new(1.7*n, 2.7)
    for i, it in enumerate(items):
        obj, kind = it[0], it[1]
        cx = i*2.3 + 1.15
        _mini_shape(ax, cx, 1.75, kind, s=0.62)
        ax.text(cx, 0.7, obj, fontsize=12, color=TXT, ha='center',
                fontweight='bold')
    if caption:
        ax.text(n*1.15, 0.05, caption, fontsize=10.5, color=GRAY, ha='center')
    ax.set_xlim(0, n*2.3); ax.set_ylim(-0.1, 2.85)
    return _save(fig, name)

def shapes_chart(name, caption=None):
    """六種四邊形家族小卡參考圖。"""
    data = [('箏形', 'kite'), ('菱形', 'rhombus'), ('長方形', 'rect'),
            ('正方形', 'square'), ('梯形', 'trap'), ('平行四邊形', 'para')]
    fig, ax = _new(6.6, 2.5)
    if caption:
        ax.text(len(data)*1.05, 2.55, caption, fontsize=11, color=GRAY,
                ha='center', fontweight='bold')
    for i, (nm, kind) in enumerate(data):
        cx = i*2.1 + 1.0
        _mini_shape(ax, cx, 1.5, kind, s=0.58)
        ax.text(cx, 0.45, nm, fontsize=11.5, color=TXT, ha='center',
                fontweight='bold')
    ax.set_xlim(0, len(data)*2.1); ax.set_ylim(0.1, 2.75)
    return _save(fig, name)

def two_transversals(name, a1='100°', a2='127°', caption=None):
    """兩平行線 + 兩條截線 M1,M2，標 ∠1∠2∠3∠4（C卷計算題）。"""
    fig, ax = _new(3.8, 2.8)
    y1, y2 = 2.1, 0.4
    ax.plot([-0.3, 3.8], [y1, y1], color=EDGE, lw=2.4, zorder=2)
    ax.plot([-0.3, 3.8], [y2, y2], color=EDGE, lw=2.4, zorder=2)
    ax.text(3.9, y1, r'$L_1$', color=EDGE, fontsize=12, va='center', fontweight='bold')
    ax.text(3.9, y2, r'$L_2$', color=EDGE, fontsize=12, va='center', fontweight='bold')
    # 兩條截線
    def line(x_top, x_bot, lab, lx):
        ax.plot([x_top, x_bot], [y1+0.45, y2-0.35], color=RED, lw=2.2, zorder=3)
        ax.text(lx, y1+0.58, lab, color=RED, fontsize=11, fontweight='bold')
    line(1.0, 0.6, r'$M_1$', 0.85)
    line(2.7, 2.35, r'$M_2$', 2.62)
    ax.text(0.35, (y1+y2)/2, r'$L_1 /\!/ L_2$', color=EDGE, fontsize=11,
            fontweight='bold', rotation=90, va='center')
    # 角標：∠1 在 M1 上線下方右, ∠2 在 M2 上線下方右, ∠3,∠4 在下線
    ax.text(1.0, y1-0.28, '∠1=' + a1, color='#c0392b', fontsize=11,
            ha='left', fontweight='bold')
    ax.text(2.55, y1-0.28, '∠2=' + a2, color='#c0392b', fontsize=11,
            ha='left', fontweight='bold')
    ax.text(0.55, y2+0.18, '∠3', color='#2e6da4', fontsize=12,
            ha='left', fontweight='bold')
    ax.text(2.3, y2+0.18, '∠4', color='#2e6da4', fontsize=12, ha='left',
            fontweight='bold')
    ax.set_xlim(-0.4, 4.3); ax.set_ylim(-0.1, 2.95)
    if caption:
        ax.text(1.8, -0.2, caption, fontsize=10, color=GRAY, ha='center')
        ax.set_ylim(-0.45, 2.95)
    return _save(fig, name)


# ---------------------------------------------------------------------------
# 學習單專用
def trap_labeled(name, caption=None):
    """大梯形，標示 上底 / 下底 / 腰 / 腰（教學參考圖）。"""
    fig, ax = _new(4.4, 2.9)
    A, B, C, D = (1.0, 1.9), (3.0, 1.9), (3.9, 0.0), (0.1, 0.0)
    ax.add_patch(Polygon([A, B, C, D], closed=True, facecolor=FILL,
                         edgecolor=EDGE, lw=2.8, zorder=2))
    # 上底 AB
    ax.annotate('上底', xy=((A[0]+B[0])/2, A[1]), xytext=((A[0]+B[0])/2, A[1]+0.5),
                ha='center', fontsize=14, fontweight='bold', color='#c0392b',
                arrowprops=dict(arrowstyle='->', color='#c0392b', lw=1.8))
    # 下底 DC
    ax.annotate('下底', xy=((C[0]+D[0])/2, 0), xytext=((C[0]+D[0])/2, -0.55),
                ha='center', fontsize=14, fontweight='bold', color='#c0392b',
                arrowprops=dict(arrowstyle='->', color='#c0392b', lw=1.8))
    # 左腰 AD
    ax.annotate('腰', xy=((A[0]+D[0])/2, (A[1]+D[1])/2),
                xytext=((A[0]+D[0])/2-0.95, (A[1]+D[1])/2),
                ha='center', va='center', fontsize=14, fontweight='bold',
                color=GREEN, arrowprops=dict(arrowstyle='->', color=GREEN, lw=1.8))
    # 右腰 BC
    ax.annotate('腰', xy=((B[0]+C[0])/2, (B[1]+C[1])/2),
                xytext=((B[0]+C[0])/2+0.95, (B[1]+C[1])/2),
                ha='center', va='center', fontsize=14, fontweight='bold',
                color=GREEN, arrowprops=dict(arrowstyle='->', color=GREEN, lw=1.8))
    ax.set_xlim(-1.4, 5.3); ax.set_ylim(-1.0, 2.6)
    if caption:
        ax.text(1.95, -0.95, caption, fontsize=11, color=GRAY, ha='center')
    return _save(fig, name)

def pick_shapes(name, items, caption=None):
    """一排有編號的圖形，讓學生圈出/打勾。items: list of (編號, kind)。"""
    n = len(items)
    fig, ax = _new(1.55*n, 2.5)
    for i, (num, kind) in enumerate(items):
        cx = i*2.2 + 1.1
        ax.add_patch(Circle((cx, 2.1), 0.26, facecolor='white',
                            edgecolor=TXT, lw=1.8, zorder=4))
        ax.text(cx, 2.1, str(num), fontsize=14, fontweight='bold', color=TXT,
                ha='center', va='center', zorder=5)
        if kind == 'tri':
            _mini_shape_tri(ax, cx, 1.15, s=0.62)
        else:
            _mini_shape(ax, cx, 1.15, kind, s=0.62)
    if caption:
        ax.text(n*1.1, 0.05, caption, fontsize=10.5, color=GRAY, ha='center')
    ax.set_xlim(0, n*2.2); ax.set_ylim(-0.1, 2.5)
    return _save(fig, name)

def _mini_shape_tri(ax, cx, cy, s=0.6, col=EDGE):
    pts = [(cx, cy+0.8*s), (cx+0.85*s, cy-0.7*s), (cx-0.85*s, cy-0.7*s)]
    ax.add_patch(Polygon(pts, closed=True, facecolor=FILL, edgecolor=col,
                         lw=2.4, zorder=2))


if __name__ == '__main__':
    quad('sample_para.png', kind='para', side_labels={'AD': '8', 'AB': '5'},
         caption='平行四邊形 ABCD')
    parallel_lines('sample_parallel.png', show_numbers=True)
    sticks('sample_sticks.png',
           [('(a) 5,7,10', [5, 7, 10]), ('(b) 3,4,8', [3, 4, 8]),
            ('(c) 6,6,11', [6, 6, 11])],
           caption='兩短邊相加 > 最長邊 才能組成三角形')
    print('OK samples done')

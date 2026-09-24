# -*- coding: utf-8 -*-
# 2026-09-10 の加筆（ChatGPT指摘の反映）で新しく必要になった図を TikZ で自作する。
#   n14_refl        … 14.8 波の反射（平面波の波面が壁で反射する。入射角 i ＝ 反射角 j）
#   n14_refr        … 14.8 波の屈折（v1>v2 の境界で波面の向きと間隔が変わる）
#   n16_interf_beat … 16.2 干渉（2音源の同心円＝場所で強弱）とうなり（時間で強弱）の対比
#   n16_quincke     … 16.2 クインケ管（スライドを d 引き出すと経路差は 2d 増える）
#   n18_mirror      … 18.2 鏡像 S' と，鏡について経路を折り返すと直線になること
#   n18_mirror_rot  … 18.2 鏡を θ 回すと反射光は 2θ 振れる
#
# pdflatex + standalone なので図中に日本語は書けない（ラベルはすべて記号）。
# 出力は fig/*.png（600dpi グレースケール）＋ extractbb で .xbb。
import subprocess, os, sys, math

TMPD = ('/private/tmp/claude-501/-Users-yutaka-Documents-Claude-Code----math-tex-tool/'
        'ead074c3-cffd-423f-8934-8a1c9648b2c5/scratchpad/tikz_kahitsu')
os.makedirs(TMPD, exist_ok=True)

HEAD = r'''\documentclass[border=3pt]{standalone}
\usepackage{amsmath}
\usepackage{tikz}
\usetikzlibrary{arrows.meta,patterns}
\begin{document}
\begin{tikzpicture}[line join=round,
   ax/.style={line width=0.7pt},
   wall/.style={line width=1.1pt},
   ray/.style={-{Latex[length=1.9mm]},line width=0.8pt},
   plain/.style={line width=0.8pt},
   wf/.style={line width=0.5pt},
   nrm/.style={line width=0.45pt,densely dashed},
   ext/.style={line width=0.5pt,densely dashed},
   arc/.style={line width=0.45pt},
   lb/.style={fill=white,inner sep=1.2pt}]
'''
TAIL = r'''\end{tikzpicture}
\end{document}
'''


def hatch(x0, x1, y, n=14, dx=0.22, dy=-0.26):
    """壁・境界の下側に斜線ハッチを引く。"""
    s = ''
    for k in range(n):
        x = x0 + (x1 - x0) * k / (n - 1.0)
        s += '\\draw[wf] (%.3f,%.3f) -- (%.3f,%.3f);\n' % (x, y, x + dx, y + dy)
    return s


def wavefronts(px, py, ux, uy, ts, half):
    """光線上の点 (px,py)+t*(ux,uy) を中心に，進行方向に垂直な波面を引く。"""
    nx, ny = -uy, ux
    s = ''
    for t in ts:
        cx, cy = px + ux * t, py + uy * t
        s += '\\draw[wf] (%.3f,%.3f) -- (%.3f,%.3f);\n' % (
            cx - nx * half, cy - ny * half, cx + nx * half, cy + ny * half)
    return s


# ---------------------------------------------------------------------------
# 14.8 反射：入射角 i ＝ 反射角 j。波面が壁について対称になっていることを見せる。
def fig_refl():
    i = math.radians(36.0)
    O = (3.0, 0.0)
    L = 3.9
    uin = (math.sin(i), -math.cos(i))            # 入射の進行方向
    uout = (math.sin(i), math.cos(i))            # 反射の進行方向
    Sin = (O[0] - uin[0] * L, O[1] - uin[1] * L)  # 入射光線の始点
    Pout = (O[0] + uout[0] * L, O[1] + uout[1] * L)

    s = '\\draw[wall] (-0.15,0) -- (6.15,0);\n'
    s += hatch(-0.15, 6.15, 0.0)
    s += '\\draw[nrm] (%.3f,-0.05) -- (%.3f,3.5);\n' % (O[0], O[0])
    # 波面（入射側・反射側）。法線をまたがないよう短めにする
    s += wavefronts(O[0], O[1], -uin[0], -uin[1], [1.45, 2.35, 3.25], 0.55)
    s += wavefronts(O[0], O[1], uout[0], uout[1], [1.45, 2.35, 3.25], 0.55)
    # 光線
    s += '\\draw[ray] (%.3f,%.3f) -- (%.3f,%.3f);\n' % (Sin[0], Sin[1], O[0], O[1])
    s += '\\draw[ray] (%.3f,%.3f) -- (%.3f,%.3f);\n' % (O[0], O[1], Pout[0], Pout[1])
    # 角度の弧（法線＝90度 から測る）
    a_in = math.degrees(math.atan2(-uin[1], -uin[0]))   # 入射光線が来る向き
    a_out = math.degrees(math.atan2(uout[1], uout[0]))
    s += '\\draw[arc] (%.3f,%.3f) ++(90:0.90) arc (90:%.2f:0.90);\n' % (O[0], O[1], a_in)
    s += '\\draw[arc] (%.3f,%.3f) ++(90:0.90) arc (90:%.2f:0.90);\n' % (O[0], O[1], a_out)
    s += '\\node[lb] at (%.3f,%.3f) {$i$};\n' % (O[0] - 0.40, 0.98)
    s += '\\node[lb] at (%.3f,%.3f) {$j$};\n' % (O[0] + 0.40, 0.98)
    return s


# ---------------------------------------------------------------------------
# 14.8 屈折：v1 > v2。振動数が不変なので波長も v に比例して変わる（波面の間隔）。
def fig_refr():
    i = math.radians(42.0)
    r = math.asin(math.sin(i) * 0.62)            # v2/v1 = 0.62
    O = (3.0, 0.0)
    uin = (math.sin(i), -math.cos(i))
    uout = (math.sin(r), -math.cos(r))
    lam1, lam2 = 0.90, 0.90 * 0.62
    Sin = (O[0] - uin[0] * 3.5, O[1] - uin[1] * 3.5)
    Pout = (O[0] + uout[0] * 3.0, O[1] + uout[1] * 3.0)

    s = '\\draw[wall] (-0.15,0) -- (6.15,0);\n'
    s += '\\draw[nrm] (%.3f,-3.1) -- (%.3f,3.2);\n' % (O[0], O[0])
    s += wavefronts(O[0], O[1], -uin[0], -uin[1], [lam1 * k for k in (1, 2, 3)], 0.55)
    s += wavefronts(O[0], O[1], uout[0], uout[1], [lam2 * k for k in (1, 2, 3, 4)], 0.50)
    s += '\\draw[ray] (%.3f,%.3f) -- (%.3f,%.3f);\n' % (Sin[0], Sin[1], O[0], O[1])
    s += '\\draw[ray] (%.3f,%.3f) -- (%.3f,%.3f);\n' % (O[0], O[1], Pout[0], Pout[1])
    a_in = math.degrees(math.atan2(-uin[1], -uin[0]))
    a_out = math.degrees(math.atan2(uout[1], uout[0]))
    s += '\\draw[arc] (%.3f,%.3f) ++(90:0.85) arc (90:%.2f:0.85);\n' % (O[0], O[1], a_in)
    s += '\\draw[arc] (%.3f,%.3f) ++(-90:0.85) arc (-90:%.2f:0.85);\n' % (O[0], O[1], a_out)
    # 角度のラベルは弧の「内側」の中心方向に置く（弧に重ならないよう半径は弧より小さく）
    mid_in = math.radians((90 + a_in) / 2)
    mid_out = math.radians((270 + (a_out + 360 if a_out < 0 else a_out)) / 2)
    s += '\\node[lb] at (%.3f,%.3f) {$i$};\n' % (
        O[0] + 0.50 * math.cos(mid_in), O[1] + 0.50 * math.sin(mid_in))
    s += '\\node[lb] at (%.3f,%.3f) {$r$};\n' % (
        O[0] + 0.48 * math.cos(mid_out), O[1] + 0.48 * math.sin(mid_out))
    # ラベルは波面・光線を避けて，境界のすぐ上下の左端の空きに置く
    s += '\\node[anchor=west] at (-0.05,0.42) {$v_1,\\ \\lambda_1$};\n'
    s += '\\node[anchor=west] at (-0.05,-0.55) {$v_2,\\ \\lambda_2$};\n'
    s += '\\node[anchor=east] at (6.10,2.70) {$v_1>v_2$};\n'
    return s


# ---------------------------------------------------------------------------
# 16.2 干渉とうなりの対比。
#   上：2音源の同心円（山の波面）。交点＝山と山が重なる点＝強め合う点に●。
#       強弱のパターンは空間に固定されている＝「場所」で決まる。
#   下：うなりの波形。同じ場所で「時間」とともに強弱が変わる。
def fig_interf_beat():
    lam = 0.78
    S1, S2 = (-1.30, 0.0), (1.30, 0.0)
    rmax = 5
    s = '\\begin{scope}[shift={(0,1.05)}]\n'
    s += '\\begin{scope}\n\\clip (-3.25,-0.12) rectangle (3.25,2.15);\n'
    for k in range(1, rmax + 1):
        s += '\\draw[wf] (%.2f,%.2f) circle (%.3f);\n' % (S1[0], S1[1], lam * k)
        s += '\\draw[wf] (%.2f,%.2f) circle (%.3f);\n' % (S2[0], S2[1], lam * k)
    # 円どうしの交点（＝山と山の重なり＝強め合う点）
    d = S2[0] - S1[0]
    for m in range(1, rmax + 1):
        for n in range(1, rmax + 1):
            r1, r2 = lam * m, lam * n
            if r1 + r2 <= d or abs(r1 - r2) >= d:
                continue
            a = (r1 * r1 - r2 * r2 + d * d) / (2 * d)
            h2 = r1 * r1 - a * a
            if h2 <= 0:
                continue
            x, y = S1[0] + a, math.sqrt(h2)
            if -3.15 < x < 3.15 and 0.05 < y < 2.08:
                s += '\\fill (%.3f,%.3f) circle (0.055);\n' % (x, y)
    s += '\\end{scope}\n'
    s += '\\fill (%.2f,%.2f) circle (0.075);\n' % S1
    s += '\\fill (%.2f,%.2f) circle (0.075);\n' % S2
    s += '\\node[anchor=north] at (%.2f,-0.10) {$\\mathrm{S_1}$};\n' % S1[0]
    s += '\\node[anchor=north] at (%.2f,-0.10) {$\\mathrm{S_2}$};\n' % S2[0]
    s += '\\end{scope}\n'

    # 下段：うなり
    s += '\\begin{scope}[shift={(0,-1.35)}]\n'
    s += '\\draw[ax,-{Latex[length=1.7mm]}] (-3.25,0) -- (3.35,0) node[anchor=west] {$t$};\n'
    pts, up, dn = [], [], []
    N = 460
    A = 0.82
    for k in range(N + 1):
        t = -3.1 + 6.2 * k / N
        env = math.cos(math.pi * t / 3.1 * 1.5)
        pts.append((t, A * env * math.cos(2 * math.pi * t * 2.15)))
        up.append((t, A * env))
        dn.append((t, -A * env))
    s += '\\draw[plain] ' + ' -- '.join('(%.3f,%.3f)' % p for p in pts) + ';\n'
    s += '\\draw[ext] ' + ' -- '.join('(%.3f,%.3f)' % p for p in up) + ';\n'
    s += '\\draw[ext] ' + ' -- '.join('(%.3f,%.3f)' % p for p in dn) + ';\n'
    s += '\\end{scope}\n'
    return s


# ---------------------------------------------------------------------------
# 16.2 クインケ管。スライドを d 引き出すと，その経路は行き帰りで d ずつ延びる → 経路差 2d。
def fig_quincke():
    xa, xb = 1.25, 4.15
    ytop, ybase, d = 1.05, -0.95, 0.80
    yb2 = ybase - d
    xm = (xa + xb) / 2
    s = ''
    # 入口・出口の管
    s += '\\draw[plain] (-0.05,0) -- (%.2f,0);\n' % xa
    s += '\\draw[plain] (%.2f,0) -- (5.45,0);\n' % xb
    # 上の経路（固定）
    s += ('\\draw[plain,rounded corners=3pt] (%.2f,0) -- (%.2f,%.2f) -- (%.2f,%.2f) -- (%.2f,0);\n'
          % (xa, xa, ytop, xb, ytop, xb))
    # 下の経路（スライド前＝点線／スライド後＝実線）
    s += ('\\draw[ext,rounded corners=3pt] (%.2f,0) -- (%.2f,%.2f) -- (%.2f,%.2f) -- (%.2f,0);\n'
          % (xa, xa, ybase, xb, ybase, xb))
    s += ('\\draw[plain,rounded corners=3pt] (%.2f,%.2f) -- (%.2f,%.2f) -- (%.2f,%.2f) -- (%.2f,%.2f);\n'
          % (xa, ybase, xa, yb2, xb, yb2, xb, ybase))
    # 分岐点・合流点
    s += '\\fill (%.2f,0) circle (0.075);\n' % xa
    s += '\\fill (%.2f,0) circle (0.075);\n' % xb
    # 経路が2本あることを矢印で示す
    s += '\\draw[ray] (%.2f,%.2f) -- (%.2f,%.2f);\n' % (xm - 0.45, ytop, xm + 0.45, ytop)
    s += '\\draw[ray] (%.2f,%.2f) -- (%.2f,%.2f);\n' % (xm - 1.05, yb2, xm - 0.15, yb2)
    # 引き出し量 d
    s += ('\\draw[{Latex[length=1.5mm]}-{Latex[length=1.5mm]},line width=0.5pt] '
          '(%.2f,%.2f) -- (%.2f,%.2f);\n' % (xm + 0.75, ybase, xm + 0.75, yb2))
    s += '\\node[anchor=west,lb] at (%.2f,%.2f) {$d$};\n' % (xm + 0.85, (ybase + yb2) / 2)
    # 入口・出口の音の向き
    s += '\\draw[ray] (0.05,0.30) -- (0.95,0.30);\n'
    s += '\\draw[ray] (4.55,0.30) -- (5.40,0.30);\n'
    s += '\\node[anchor=south] at (0.50,0.38) {$\\mathrm{A}$};\n'
    s += '\\node[anchor=south] at (4.98,0.38) {$\\mathrm{B}$};\n'
    return s


# ---------------------------------------------------------------------------
# 18.2 鏡像と折り返し。S' は S の鏡像。S→Q→P の経路長は S'P に等しい。
def fig_mirror():
    S = (1.25, 2.15)
    P = (4.35, 1.45)
    Sp = (S[0], -S[1])
    t = (0 - Sp[1]) / (P[1] - Sp[1])
    Q = (Sp[0] + t * (P[0] - Sp[0]), 0.0)

    s = '\\draw[wall] (-0.10,0) -- (5.30,0);\n'
    s += hatch(-0.10, 5.30, 0.0, n=13)
    s += '\\node[anchor=north west] at (5.30,-0.05) {$\\mathrm{M}$};\n'
    s += '\\draw[nrm] (%.3f,-0.05) -- (%.3f,2.45);\n' % (Q[0], Q[0])
    s += '\\draw[ray] (%.3f,%.3f) -- (%.3f,%.3f);\n' % (S[0], S[1], Q[0], Q[1])
    s += '\\draw[ray] (%.3f,%.3f) -- (%.3f,%.3f);\n' % (Q[0], Q[1], P[0], P[1])
    s += '\\draw[ext] (%.3f,%.3f) -- (%.3f,%.3f);\n' % (Sp[0], Sp[1], Q[0], Q[1])
    s += '\\draw[ext] (%.3f,%.3f) -- (%.3f,%.3f);\n' % (S[0], S[1], Sp[0], Sp[1])
    s += '\\fill (%.3f,%.3f) circle (0.065);\n' % S
    s += '\\fill (%.3f,%.3f) circle (0.065);\n' % P
    s += '\\fill (%.3f,%.3f) circle (0.065);\n' % Q
    s += '\\draw[plain] (%.3f,%.3f) circle (0.075);\n' % Sp
    s += '\\node[anchor=east] at (%.3f,%.3f) {$\\mathrm{S}$};\n' % (S[0] - 0.10, S[1])
    s += '\\node[anchor=west] at (%.3f,%.3f) {$\\mathrm{P}$};\n' % (P[0] + 0.10, P[1])
    s += '\\node[anchor=north east,lb] at (%.3f,%.3f) {$\\mathrm{Q}$};\n' % (Q[0] - 0.06, -0.10)
    s += '\\node[anchor=east] at (%.3f,%.3f) {$\\mathrm{S}^\\prime$};\n' % (Sp[0] - 0.12, Sp[1])
    # 等距離の印
    for yy, sg in ((S[1] / 2, 1), (-S[1] / 2, 1)):
        s += '\\draw[wf] (%.3f,%.3f) -- (%.3f,%.3f);\n' % (S[0] - 0.11, yy - 0.09, S[0] + 0.11, yy + 0.09)
    # 入射角・反射角
    aS = math.degrees(math.atan2(S[1] - Q[1], S[0] - Q[0]))
    aP = math.degrees(math.atan2(P[1] - Q[1], P[0] - Q[0]))
    s += '\\draw[arc] (%.3f,%.3f) ++(90:0.95) arc (90:%.2f:0.95);\n' % (Q[0], Q[1], aS)
    s += '\\draw[arc] (%.3f,%.3f) ++(90:0.95) arc (90:%.2f:0.95);\n' % (Q[0], Q[1], aP)
    s += '\\node at (%.3f,%.3f) {\\footnotesize $i$};\n' % (Q[0] - 0.46, 1.02)
    s += '\\node at (%.3f,%.3f) {\\footnotesize $j$};\n' % (Q[0] + 0.44, 1.05)
    return s


# ---------------------------------------------------------------------------
# 18.2 鏡を θ 回すと反射光は 2θ 振れる。入射光線は固定。
def fig_mirror_rot():
    th = math.radians(21.0)
    i = math.radians(40.0)
    L = 2.45
    d = (math.sin(i), -math.cos(i))              # 入射の進行方向
    A = (-d[0] * L, -d[1] * L)                   # 入射光線の始点

    def reflect(n):
        dot = d[0] * n[0] + d[1] * n[1]
        return (d[0] - 2 * dot * n[0], d[1] - 2 * dot * n[1])

    r1 = reflect((0.0, 1.0))
    r2 = reflect((-math.sin(th), math.cos(th)))

    s = '\\draw[wall] (-2.15,0) -- (2.15,0);\n'
    s += hatch(-2.15, 2.15, 0.0, n=11, dx=0.18, dy=-0.21)
    # 回転後の鏡。左半分まで描くと壁のハッチと交差して読みにくいので右半分だけにする
    s += '\\draw[plain,densely dashed] (0,0) -- (%.3f,%.3f);\n' % (
        2.15 * math.cos(th), 2.15 * math.sin(th))
    s += '\\draw[ray] (%.3f,%.3f) -- (0,0);\n' % A
    s += '\\draw[ray] (0,0) -- (%.3f,%.3f);\n' % (r1[0] * L, r1[1] * L)
    s += '\\draw[ray] (0,0) -- (%.3f,%.3f);\n' % (r2[0] * L * 1.05, r2[1] * L * 1.05)
    a1 = math.degrees(math.atan2(r1[1], r1[0]))
    a2 = math.degrees(math.atan2(r2[1], r2[0]))
    s += '\\draw[arc] (0,0) ++(0:1.62) arc (0:%.2f:1.62);\n' % math.degrees(th)
    s += '\\draw[arc] (0,0) ++(%.2f:2.05) arc (%.2f:%.2f:2.05);\n' % (a1, a1, a2)
    s += '\\node at (%.2f:1.90) {\\footnotesize $\\theta$};\n' % (math.degrees(th) / 2)
    s += '\\node at (%.2f:2.32) {\\footnotesize $2\\theta$};\n' % ((a1 + a2) / 2)
    return s


FIGS = {
    'n14_refl':        fig_refl,
    'n14_refr':        fig_refr,
    'n16_interf_beat': fig_interf_beat,
    'n16_quincke':     fig_quincke,
    'n18_mirror':      fig_mirror,
    'n18_mirror_rot':  fig_mirror_rot,
}


def build(name, body):
    tex = os.path.join(TMPD, name + '.tex')
    open(tex, 'w', encoding='utf-8').write(HEAD + body + TAIL)
    r = subprocess.run(['pdflatex', '-interaction=nonstopmode', '-output-directory', TMPD, tex],
                       capture_output=True, text=True)
    pdf = os.path.join(TMPD, name + '.pdf')
    if not os.path.exists(pdf):
        print('  !! コンパイル失敗', name)
        print('\n'.join(l for l in r.stdout.splitlines() if l.startswith('!'))[:900])
        return
    out = 'fig/%s.png' % name
    subprocess.run(['gs', '-sDEVICE=pnggray', '-r600', '-dNOPAUSE', '-dBATCH', '-o', out, pdf],
                   capture_output=True)
    subprocess.run(['extractbb', out], capture_output=True)
    print('  %-20s %6.1f KB' % (os.path.basename(out), os.path.getsize(out) / 1000))


if __name__ == '__main__':
    os.chdir('/Users/yutaka/Documents/入試物理基礎演習')
    only = sys.argv[1:] or None
    for n, f in FIGS.items():
        if only and not any(k in n for k in only):
            continue
        build(n, f())

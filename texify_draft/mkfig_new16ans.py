# -*- coding: utf-8 -*-
# 新第16回の例題の「解答図」をTikZで自作する。
# 原本の例題には解答が載っていないため解答図も存在しない（組版チェックリスト 2. の方針）。
# pdflatex を使うので図中に日本語は書けない。ラベルはすべて記号にしてある。
#   n16_ex11_modes      例題11(1)(6) 閉管の3つの定在波（●＝疎密変化が最大＝変位の節）
#   n16_ex11_p3         例題11(7)    3倍振動のある瞬間の変位と圧力の高低
#   n16_ex12_two        例題12(1)    共鳴管：l1（基本振動）と l2（3倍振動）＋開口端補正 ε
# _blank は穴埋め版用（答えの線を \path にして寸法だけ同じにしたもの）。
import subprocess, os, math

TMPD = '/private/tmp/claude-501/-Users-yutaka-Documents-Claude-Code----math-tex-tool/eac48c81-c173-4fc8-82ff-b0fd70232fcb/scratchpad/tikz16'
os.makedirs(TMPD, exist_ok=True)

HEAD = r'''\documentclass[border=3pt]{standalone}
\usepackage{amsmath,amssymb}
\usepackage{tikz}
\usetikzlibrary{arrows.meta,patterns}
\begin{document}
\begin{tikzpicture}[x=0.30cm,y=0.30cm,line join=round,
   tube/.style={line width=0.9pt},
   cv/.style={line width=1.1pt},
   cvd/.style={line width=0.8pt,densely dashed},
   dim/.style={{Latex[length=1.6mm]}-{Latex[length=1.6mm]},line width=0.4pt},
   gd/.style={line width=0.3pt,densely dashed},
   arr/.style={-{Latex[length=1.6mm]},line width=0.6pt}]
'''
TAIL = r'''\end{tikzpicture}
\end{document}
'''
FIGS = {}


def poly(pts, style, hide=False):
    # 穴埋め版は opacity=0 で描く。インクは出ないが線幅ごと bbox に効くので
    # 完全版とバウンディングボックスが1ptもずれない（\path だと線幅の分だけ縮む）。
    # 白で描くと下にある線（弦の直線など）を消してしまうので使わない。
    if hide: style += ',opacity=0'
    return '\\draw[%s] %s;\n' % (style, ' -- '.join('(%.3f,%.3f)' % p for p in pts))


# ===== 例題11 (1)(6) 閉管の3つの定在波 =======================================
# 管は水平．左端＝閉端（節），右端＝開端（腹）．長さ L=20（作図単位）．
L, A, HH = 30.0, 2.1, 3.2   # 管の長さ・振幅・管の内側の半分の高さ

def modes(hide=False):
    s = ''
    for k, (m, y0) in enumerate(((1, 0.0), (3, -9.5), (5, -19.0))):
        # 管（上下の壁と左の閉端）
        s += '\\draw[tube] (0,%.2f) -- (%.2f,%.2f);\n' % (y0 + HH, L, y0 + HH)
        s += '\\draw[tube] (0,%.2f) -- (%.2f,%.2f);\n' % (y0 - HH, L, y0 - HH)
        s += '\\draw[tube] (0,%.2f) -- (0,%.2f);\n' % (y0 - HH, y0 + HH)
        # 定在波（横波表示）：閉端が節，開端が腹  y = A sin(m*pi*x/(2L))
        for sgn, st in ((1, 'cv'), (-1, 'cvd')):
            pts = []
            x = 0.0
            while x <= L + 1e-9:
                pts.append((x, y0 + sgn * A * math.sin(m * math.pi * x / (2 * L))))
                x += L / 200.0
            s += poly(pts, st, hide)
        # 節（＝疎密変化が最大の点）に●
        j = 0
        while True:
            xn = 2.0 * j * L / m          # sin=0 となる点 x = 2jL/m
            if xn > L + 1e-9: break
            s += '\\draw[fill=black%s] (%.3f,%.2f) circle (0.42);\n' % (
                ',opacity=0' if hide else '', xn, y0)
            j += 1
        # ラベル
        s += '\\node[left] at (-1.6,%.2f) {\\textcircled{\\scriptsize %d}};\n' % (y0, k + 1)
        # 管の長さ l
        s += '\\draw[dim] (0,%.2f) -- (%.2f,%.2f);\n' % (y0 + HH + 1.5, L, y0 + HH + 1.5)
        s += '\\node[above,inner sep=1pt] at (%.2f,%.2f) {$l$};\n' % (L / 2, y0 + HH + 1.3)
    return s

FIGS['n16_ex11_modes'] = modes(False)
FIGS['n16_ex11_modes_blank'] = modes(True)


# ===== 例題11 (7) 3倍振動の圧力 =============================================
# 穴埋め版は「管と波形だけ」を残し，変位の矢印・節の●・P_max/P_min・2l/3 の寸法を
# 白（＝見えないが bbox は同じ）にして，生徒が書き込めるようにする。
def press(hide=False):
    W = ',opacity=0' if hide else ''
    s = ''
    m, y0 = 3, 0.0
    s += '\\draw[tube] (0,%.2f) -- (%.2f,%.2f);\n' % (y0 + HH, L, y0 + HH)
    s += '\\draw[tube] (0,%.2f) -- (%.2f,%.2f);\n' % (y0 - HH, L, y0 - HH)
    s += '\\draw[tube] (0,%.2f) -- (0,%.2f);\n' % (y0 - HH, y0 + HH)
    pts = []
    x = 0.0
    while x <= L + 1e-9:
        pts.append((x, A * math.sin(m * math.pi * x / (2 * L))))
        x += L / 200.0
    s += poly(pts, 'cv')
    # 変位の向きを表す矢印（横波表示の y の符号＝管の軸方向の変位）
    for xa in (3.0, 6.0, 9.0, 13.5, 16.5, 23.0, 26.0, 29.0):
        y = A * math.sin(m * math.pi * xa / (2 * L))
        d = 1.6 if y > 0 else -1.6
        s += '\\draw[arr%s] (%.2f,%.2f) -- (%.2f,%.2f);\n' % (W, xa, -HH - 1.6, xa + d, -HH - 1.6)
    # 節（圧力変動の腹）
    s += '\\draw[fill=black%s] (0,0) circle (0.42);\n' % W
    s += '\\draw[fill=black%s] (%.3f,0) circle (0.42);\n' % (W, 2.0 * L / 3.0)
    s += '\\node[below left=1pt%s] at (0,%.2f) {$P_{\\min}$};\n' % (W, -HH - 3.2)
    s += '\\node[below%s] at (%.3f,%.2f) {$P_{\\max}$};\n' % (W, 2.0 * L / 3.0, -HH - 3.2)
    s += '\\draw[gd%s] (0,%.2f) -- (0,%.2f);\n' % (W, -HH - 1.0, -HH - 3.0)
    s += '\\draw[gd%s] (%.3f,%.2f) -- (%.3f,%.2f);\n' % (W, 2.0 * L / 3.0, -HH - 1.0, 2.0 * L / 3.0, -HH - 3.0)
    s += '\\draw[dim%s] (0,%.2f) -- (%.3f,%.2f);\n' % (W, HH + 1.5, 2.0 * L / 3.0, HH + 1.5)
    s += '\\node[above,inner sep=1pt%s] at (%.3f,%.2f) {$\\frac{2}{3}l$};\n' % (W, L / 3.0, HH + 1.3)
    return s

FIGS['n16_ex11_p3'] = press(False)
FIGS['n16_ex11_p3_blank'] = press(True)


# ===== 例題10 (2)(3) 弦に生じる定在波 ========================================
# 原本の解答図（練習［24］のもの）を流用していたが，穴埋め版で「波形を描かせる」ため
# TikZ で描き直した。blank は弦の直線と寸法線だけを残す。
GL, GA = 30.0, 2.6          # 弦の長さ・振幅（作図単位）

def gen(nloop, lab, dimlam=False, hide=False):
    # 貼付幅が62〜75mmと小さく，標準の線幅(0.3〜0.4pt)だと縮小後に消えかけるので太めにする
    s = ''
    # 両端の節を示す縦の破線
    for x in (0.0, GL):
        s += '\\draw[gd,line width=0.5pt] (%.2f,%.2f) -- (%.2f,%.2f);\n' % (x, -GA - 1.2, x, GA + 1.2)
    for sgn, st in ((1, 'cv'), (-1, 'cvd')):
        pts = []
        x = 0.0
        while x <= GL + 1e-9:
            pts.append((x, sgn * GA * math.sin(nloop * math.pi * x / GL)))
            x += GL / 300.0
        s += poly(pts, st, hide)
    # 弦の静止位置（波の後に描く）と長さの寸法線
    s += '\\draw[line width=0.6pt] (0,0) -- (%.2f,0);\n' % GL
    s += '\\draw[dim,line width=0.6pt] (0,%.2f) -- (%.2f,%.2f);\n' % (-GA - 2.0, GL, -GA - 2.0)
    s += '\\node[below,inner sep=1pt] at (%.2f,%.2f) {$%s$};\n' % (GL / 2, -GA - 2.2, lab)
    if dimlam:      # 節−節間隔 λ/2
        x1 = GL / nloop
        W = ',opacity=0' if hide else ''
        s += '\\draw[dim,line width=0.6pt%s] (0,%.2f) -- (%.2f,%.2f);\n' % (W, GA + 1.6, x1, GA + 1.6)
        s += '\\node[above,inner sep=1pt%s] at (%.2f,%.2f) {$\\lambda/2$};\n' % (
            W, x1 / 2, GA + 1.4)
    return s

FIGS['n16_ex10_fund'] = gen(1, 'l')
FIGS['n16_ex10_fund_blank'] = gen(1, 'l', hide=True)
FIGS['n16_ex10_n'] = gen(5, 'l', dimlam=True)
FIGS['n16_ex10_n_blank'] = gen(5, 'l', dimlam=True, hide=True)


# ===== 例題12 (1) 共鳴管の2つの共鳴 ==========================================
# 縦の管．上端＝開口．腹は開口より eps だけ上．水面が節．
LAM, EPS, AMP, RW = 12.0, 1.4, 2.4, 3.4     # 波長・開口端補正・振幅・管の半幅

def tube(x0, depth, nlab, hide=False):
    """x0 を管の中心軸として，開口から depth（＝l+eps−eps）の水面までの管を描く。
       depth は「腹（＝開口の eps 上）から水面までの長さ」= lam/4 または 3lam/4。"""
    s = ''
    ytop = 0.0                      # 腹の高さ（y は上向き，0 が腹）
    yopen = ytop - EPS              # 開口
    ywat = ytop - depth             # 水面
    ybot = ywat - 3.0
    # 管の壁
    s += '\\draw[tube] (%.2f,%.2f) -- (%.2f,%.2f);\n' % (x0 - RW, yopen, x0 - RW, ybot)
    s += '\\draw[tube] (%.2f,%.2f) -- (%.2f,%.2f);\n' % (x0 + RW, yopen, x0 + RW, ybot)
    s += '\\draw[tube] (%.2f,%.2f) -- (%.2f,%.2f);\n' % (x0 - RW, ybot, x0 + RW, ybot)
    # 水面（水は網かけ）
    s += '\\draw[pattern=north east lines,draw=black,line width=0.5pt] (%.2f,%.2f) rectangle (%.2f,%.2f);\n' % (
        x0 - RW, ybot, x0 + RW, ywat)
    # 定在波（横波表示）：腹 y=ytop，節 y=ywat  x = AMP*cos(2pi*(ytop-y)/lam)
    for sgn, st in ((1, 'cv'), (-1, 'cvd')):
        pts = []
        t = 0.0
        while t <= depth + 1e-9:
            pts.append((x0 + sgn * AMP * math.cos(2 * math.pi * t / LAM), ytop - t))
            t += depth / 200.0
        s += poly(pts, st, hide)
    # 開口・腹の位置の補助線と eps
    s += '\\draw[gd] (%.2f,%.2f) -- (%.2f,%.2f);\n' % (x0 - RW - 1.9, ytop, x0 + RW + 0.6, ytop)
    s += '\\draw[gd] (%.2f,%.2f) -- (%.2f,%.2f);\n' % (x0 - RW - 1.9, yopen, x0 - RW, yopen)
    s += '\\draw[gd] (%.2f,%.2f) -- (%.2f,%.2f);\n' % (x0 + RW, ywat, x0 + RW + 2.6, ywat)
    s += '\\draw[dim] (%.2f,%.2f) -- (%.2f,%.2f);\n' % (x0 - RW - 1.4, ytop, x0 - RW - 1.4, yopen)
    s += '\\node[left,inner sep=2.5pt] at (%.2f,%.2f) {$\\varepsilon$};\n' % (x0 - RW - 1.4, (ytop + yopen) / 2)
    s += '\\draw[dim] (%.2f,%.2f) -- (%.2f,%.2f);\n' % (x0 + RW + 2.0, yopen, x0 + RW + 2.0, ywat)
    s += '\\node[right,inner sep=1.5pt] at (%.2f,%.2f) {$%s$};\n' % (x0 + RW + 2.0, (yopen + ywat) / 2, nlab)
    return s

def two(hide=False):
    return tube(0.0, LAM / 4.0, 'l_1', hide) + tube(22.0, 3.0 * LAM / 4.0, 'l_2', hide)

FIGS['n16_ex12_two'] = two(False)
FIGS['n16_ex12_two_blank'] = two(True)


# --------------------------------------------------------------------------
def build(name, body):
    tex = os.path.join(TMPD, name + '.tex')
    open(tex, 'w', encoding='utf-8').write(HEAD + body + TAIL)
    r = subprocess.run(['pdflatex', '-interaction=nonstopmode', '-output-directory', TMPD, tex],
                       capture_output=True, text=True)
    pdf = os.path.join(TMPD, name + '.pdf')
    if not os.path.exists(pdf):
        print('  !! コンパイル失敗', name)
        print('\n'.join(l for l in r.stdout.splitlines() if l.startswith('!'))[:800]); return
    out = 'fig/%s.png' % name
    subprocess.run(['gs', '-sDEVICE=pnggray', '-r600', '-dNOPAUSE', '-dBATCH', '-o', out, pdf],
                   capture_output=True)
    subprocess.run(['extractbb', out], capture_output=True)
    print('  %-24s %6.1f KB' % (os.path.basename(out), os.path.getsize(out) / 1000))


if __name__ == '__main__':
    os.chdir('/Users/yutaka/Documents/入試物理基礎演習')
    import sys
    only = sys.argv[1:] or None
    for n, b in FIGS.items():
        if only and not any(k in n for k in only): continue
        build(n, b)

# -*- coding: utf-8 -*-
# 新第20回の「原本に無い図」を TikZ で自作する。
#   n20_ex28_ans1/2 … 例題28（実光源）の作図の解答（(1)(2) と (3)(4)）
#   n20_ex29_ans1/2 … 例題29（虚光源）の作図の解答（(1)(2) と (3)）
#   n20_p71_zu      … 練習［71］の装置図。**原本の図は「2.0[cm]」と誤植**しており
#                     問題文の 2.0[m] と食い違うので，TikZ で描き直した。
# pdflatex なので図中に日本語は書けない（ラベルはすべて記号）。
#
# 作図の約束（原本 ㉗[60][61][62] の解答と同じ2本の光線）：
#   \MARU{1} 光軸に平行な光 … 凸レンズは向こう側の焦点 F2 を通り，
#            凹レンズは手前側の焦点 F1 から出たように進む（傾き -h/f，f は符号つき）
#   \MARU{2} レンズの中心 O を通る光 … 曲がらずに直進する
#   2本の交点が像 BB'。虚像のときは屈折光の延長（破線）の交点。
#   虚光源のときは，レンズに入る前の光が A に向かって集まっている（点線で示す）。
import subprocess, os, sys

TMPD = '/private/tmp/claude-501/-Users-yutaka-Documents-Claude-Code----math-tex-tool/160478f1-8123-47e0-a3a3-7085f6aff78c/scratchpad/tikz20'
os.makedirs(TMPD, exist_ok=True)

HEAD = r'''\documentclass[border=3pt]{standalone}
\usepackage{amsmath}
\usepackage{tikz}
\usetikzlibrary{arrows.meta}
\begin{document}
\begin{tikzpicture}[x=0.42cm,y=0.42cm,line join=round,
   ax/.style={line width=0.7pt},
   ln/.style={line width=0.9pt},
   ray/.style={line width=0.6pt},
   ext/.style={line width=0.5pt,densely dashed},
   vir/.style={line width=0.5pt,densely dotted},
   obj/.style={-{Latex[length=1.7mm]},line width=1.0pt}]
'''
TAIL = r'''\end{tikzpicture}
\end{document}
'''

H  = 1.15    # 物体の高さ
LH = 2.55    # レンズの半分の高さ
FD = 3.0     # 焦点距離の作図単位（|f| = FD）


def lens(x0, conv):
    """レンズの輪郭。conv=True で凸レンズ，False で凹レンズ。"""
    if conv:
        return ('\\draw[ln] (%.3f,%.3f) .. controls (%.3f,0) .. (%.3f,%.3f)'
                ' .. controls (%.3f,0) .. (%.3f,%.3f);\n'
                % (x0, -LH, x0 - 0.95, x0, LH, x0 + 0.95, x0, -LH))
    w = 0.55
    return ('\\draw[ln] (%.3f,%.3f) -- (%.3f,%.3f)'
            ' .. controls (%.3f,0) .. (%.3f,%.3f) -- (%.3f,%.3f)'
            ' .. controls (%.3f,0) .. (%.3f,%.3f);\n'
            % (x0 - w, LH, x0 + w, LH,
               x0 + w - 0.62, x0 + w, -LH, x0 - w, -LH,
               x0 - w + 0.62, x0 - w, LH))


def panel(x0, tag, f, a):
    """1つのパネルを描き，(TeXコード, 右端の作図座標) を返す。
       f>0 凸／f<0 凹．a>0 実光源（レンズの手前）／a<0 虚光源（レンズの奥）。
       座標はレンズの中心を原点，右向きを正にとる（x0 だけ平行移動する）。"""
    b  = 1.0 / (1.0 / f - 1.0 / a)          # 写像公式
    hi = -(b / a) * H                        # 倍率（符号つき）
    xo = -a                                  # 光源の位置
    xl = min(xo, -abs(f), b) - 1.6
    xr = max(xo,  abs(f), b) + 1.6
    s  = ''
    # 光軸とレンズと焦点
    s += '\\draw[ax] (%.3f,0) -- (%.3f,0);\n' % (x0 + xl, x0 + xr)
    s += lens(x0, f > 0)
    for sx, lab, an in ((-abs(f), 'F_1', 'above left'), (abs(f), 'F_2', 'above right')):
        s += '\\fill (%.3f,0) circle (1.5pt);\n' % (x0 + sx)
        s += '\\node[%s,inner sep=1.8pt] at (%.3f,0) {$\\mathrm{%s}$};\n' % (an, x0 + sx, lab)
    # 光源 AA'
    s += '\\draw[obj] (%.3f,0) -- (%.3f,%.3f);\n' % (x0 + xo, x0 + xo, H)
    # A と B が近いときは左右に振り分ける（B を A の反対側へ寄せる）
    left = 'left' if b > xo else 'right'          # A を寄せる向き
    right = 'right' if b > xo else 'left'         # B を寄せる向き
    s += '\\node[above %s,inner sep=1.4pt] at (%.3f,%.3f) {$\\mathrm{A}$};\n' % (left, x0 + xo, H)
    s += '\\node[below %s,inner sep=2.2pt] at (%.3f,0) {$\\mathrm{A^\\prime}$};\n' % (left, x0 + xo)
    # 光線1（光軸に平行）：入射は実光源なら A から，虚光源なら図の左端から
    x1s = xo if a > 0 else xl
    s += '\\draw[ray] (%.3f,%.3f) -- (%.3f,%.3f);\n' % (x0 + x1s, H, x0, H)
    k1 = -H / f                              # 屈折後の傾き
    s += '\\draw[ray] (%.3f,%.3f) -- (%.3f,%.3f);\n' % (x0, H, x0 + xr, H + k1 * xr)
    if f < 0:                                # 凹レンズは手前の焦点から出たように見える
        s += '\\draw[ext] (%.3f,%.3f) -- (%.3f,0);\n' % (x0, H, x0 - abs(f))
    # 光線2（レンズの中心を通る）
    k2 = H / xo
    s += '\\draw[ray] (%.3f,%.3f) -- (%.3f,%.3f);\n' % (x0 + xl, k2 * xl, x0 + xr, k2 * xr)
    # 虚光源のときは「A に向かって集まる光」であることを点線で示す
    if a < 0:
        s += '\\draw[vir] (%.3f,%.3f) -- (%.3f,%.3f);\n' % (x0, H, x0 + xo, H)
    # 像 BB'
    if b < 0:                                # 虚像 → 屈折光の延長の交点
        s += '\\draw[ext] (%.3f,%.3f) -- (%.3f,%.3f);\n' % (x0, H, x0 + b, hi)
        s += '\\draw[ext] (%.3f,0) -- (%.3f,%.3f);\n' % (x0, x0 + b, hi)
    s += '\\draw[obj] (%.3f,0) -- (%.3f,%.3f);\n' % (x0 + b, x0 + b, hi)
    pos  = ('above' if hi > 0 else 'below') + ' ' + right
    pos2 = ('below' if hi > 0 else 'above') + ' ' + right
    s += '\\node[%s,inner sep=1.4pt] at (%.3f,%.3f) {$\\mathrm{B}$};\n' % (pos, x0 + b, hi)
    s += '\\node[%s,inner sep=2.2pt] at (%.3f,0) {$\\mathrm{B^\\prime}$};\n' % (pos2, x0 + b)
    # パネル番号
    s += '\\node[anchor=north west] at (%.3f,%.3f) {(%s)};\n' % (x0 + xl, LH + 2.6, tag)
    return s, xr


def pair(p1, p2=None):
    """パネルを横に並べる。p=(tag, f, a)"""
    s, x0 = '', 0.0
    for p in (p1, p2):
        if p is None: continue
        tag, f, a = p
        xl = min(-a, abs(f), 1.0 / (1.0 / f - 1.0 / a)) - 1.6
        body, xr = panel(x0 - xl, tag, f, a)
        s += body
        x0 = x0 - xl + xr + 4.4
    return s


FIGS = {}
# 例題28（実光源）… (1) 凸 a=2.13f  (2) 凸 a=0.50f  (3) 凹 a=2.27f  (4) 凹 a=0.49f
FIGS['n20_ex28_ans1'] = pair(('1',  FD,  2.13 * FD), ('2',  FD, 0.50 * FD))
FIGS['n20_ex28_ans2'] = pair(('3', -FD,  2.27 * FD), ('4', -FD, 0.49 * FD))
# 例題29（虚光源）… (1) 凸 a=-1.45f  (2) 凹 a=-0.62f  (3) 凹 a=-1.78f
FIGS['n20_ex29_ans1'] = pair(('1',  FD, -1.45 * FD), ('2', -FD, -0.62 * FD))
FIGS['n20_ex29_ans2'] = pair(('3', -FD, -1.78 * FD))

# 練習［71］の装置図（原本の図は 2.0[cm] と誤植）
def p71():
    s  = '\\draw[ax] (-9.5,0) -- (5.0,0);\n'
    s += lens(2.4, True)
    s += '\\fill (-5.6,0) circle (1.6pt);\n'
    s += '\\node[below,inner sep=2.6pt] at (-5.6,0) {$\\mathrm{S}$};\n'
    s += '\\node[below,inner sep=2.6pt] at (-9.5,0) {$\\mathrm{L}$};\n'
    s += '\\node[below,inner sep=2.6pt] at (5.0,0) {$\\mathrm{L^\\prime}$};\n'
    s += ('\\draw[{Latex[length=1.6mm]}-{Latex[length=1.6mm]},line width=0.4pt]'
          ' (-5.6,1.9) -- (2.4,1.9);\n')
    s += '\\node[above,inner sep=1.4pt] at (-1.6,1.9) {$2.0\\,[\\mathrm{m}]$};\n'
    return s
FIGS['n20_p71_zu'] = p71()


def remake_xbb(png):
    """.xbb を作り直す。**extractbb は .xbb が .png より新しいと黙ってスキップする**ので，
       必ず消してから呼ぶ（古い .xbb が残ると画像が箱からはみ出して直前の行を塗り潰す。
       実際に fig/n20_a65_conc.xbb でこれが起き，練習［65］の解答1行目が消えていた）。"""
    xbb = png[:-4] + '.xbb'
    if os.path.exists(xbb):
        os.remove(xbb)
    subprocess.run(['extractbb', png], capture_output=True)


HEAD_JA = r"""\documentclass[border=3pt,dvipdfmx]{standalone}
\usepackage{amsmath}
\usepackage{tikz}
\usetikzlibrary{arrows.meta}
\begin{document}
\begin{tikzpicture}[line join=round,line cap=round,
   ax/.style={-{Latex[length=1.6mm]},line width=0.6pt},
   asym/.style={line width=0.4pt,densely dotted},
   cv/.style={line width=0.9pt},
   ln/.style={line width=0.8pt},
   ray/.style={line width=0.7pt},
   ext/.style={line width=0.5pt,densely dashed}]
"""


def build_ja(name, body):
    """図中に日本語を書くための uplatex + dvipdfmx 版。"""
    tex = os.path.join(TMPD, name + '.tex')
    open(tex, 'w', encoding='utf-8').write(HEAD_JA + body + TAIL)
    for _ in range(2):
        r = subprocess.run(['uplatex', '-interaction=nonstopmode', '-output-directory', TMPD, tex],
                           capture_output=True, text=True)
    dvi = os.path.join(TMPD, name + '.dvi')
    if not os.path.exists(dvi):
        print('  !! コンパイル失敗', name)
        print('\n'.join(l for l in r.stdout.splitlines() if l.startswith('!'))[:800]); return
    subprocess.run(['dvipdfmx', '-o', os.path.join(TMPD, name + '.pdf'), dvi], capture_output=True)
    out = 'fig/%s.png' % name
    subprocess.run(['gs', '-sDEVICE=pnggray', '-r600', '-dNOPAUSE', '-dBATCH', '-o', out,
                    os.path.join(TMPD, name + '.pdf')], capture_output=True)
    remake_xbb(out)
    print('  %-24s %6.1f KB' % (os.path.basename(out), os.path.getsize(out) / 1000))


# ---------------------------------------------------------------------------
#  写像公式の直角双曲線 (a-f)(b-f)=f^2
#    原本（prob2_p87）の図を切り出して使っていたが，
#      ・凹レンズ側に ● が描かれていない（解答本文は「図の●の点」と書いている）＝原本の誤り
#      ・本文 20.5 と練習［72］は例題30専用の ● 付き図を流用していて ● が意味を持たない
#    の2点があったので TikZ で描き直した（2026-09-20）。
#      n20_hyp_conv / n20_hyp_conc … ● 無し（本文 20.5・練習［72］用）
#      n20_ex30_conv / n20_ex30_conc … ● 付き（例題30用。● の座標も実際の答に合わせた）
def hyperbola(f, dot=None, dotlab=None, blank=False):
    """f=+1 で凸レンズ，f=-1 で凹レンズ。dot=(a,b) を渡すとその点に ● を打つ。
       blank=True は穴埋め版用で，● の座標を \\phantom にして消す（答が図に出てしまうため）。
       \\AnaFig は完全版と穴埋め版を同じ幅で貼るので，縦横比を変えないよう
       文字を消すのではなく \\phantom で同じ大きさの空白を残す。"""
    if blank and dotlab:
        dotlab = '\\phantom{%s}' % dotlab
    U = 0.46          # 1単位 = 0.46cm（貼り付け幅62mmでほぼ原寸になる）
    lo, hi = (-3.6, 6.6) if f > 0 else (-5.6, 5.6)
    blo, bhi = (-4.6, 6.6) if f > 0 else (-5.6, 4.6)
    s = '\\begin{scope}[x=%.3fcm,y=%.3fcm]\n' % (U, U)
    # 漸近線
    s += '\\draw[asym] (%.2f,%.2f) -- (%.2f,%.2f);\n' % (f, blo, f, bhi)
    s += '\\draw[asym] (%.2f,%.2f) -- (%.2f,%.2f);\n' % (lo, f, hi, f)
    # 座標軸
    s += '\\draw[ax] (%.2f,0) -- (%.2f,0) node[below,inner sep=2pt] {$a$};\n' % (lo, hi)
    s += '\\draw[ax] (0,%.2f) -- (0,%.2f) node[right,inner sep=2pt] {$b$};\n' % (blo, bhi)
    s += '\\node[above right,inner sep=2.5pt] at (0,0) {$\\mathrm{O}$};\n'
    # f>0 と f<0 で目盛りの向きを変える（原点近くで2つの $f$ がぶつからないように）
    s += '\\node[%s,inner sep=2.5pt] at (%.2f,0) {$f$};\n' % ('below' if f > 0 else 'above left', f)
    s += '\\node[%s,inner sep=2.5pt] at (0,%.2f) {$f$};\n' % ('left' if f > 0 else 'below left', f)
    # 双曲線の2つの枝
    def branch(a0, a1, n=80):
        pts = []
        for i in range(n + 1):
            a = a0 + (a1 - a0) * i / n
            b = f + f * f / (a - f)
            b = max(blo + 0.05, min(bhi - 0.05, b))
            pts.append('(%.3f,%.3f)' % (a, b))
        return '\\draw[cv] plot[smooth] coordinates {%s};\n' % ' '.join(pts)
    eps = 0.175
    s += branch(f + eps, hi - 0.3)          # 右上の枝
    s += branch(lo + 0.3, f - eps)          # 左下の枝
    if dot:
        s += '\\fill (%.2f,%.2f) circle (2.4pt);\n' % dot
        if dotlab:
            if f > 0:      # 右上の枝の右どなりが空いている
                s += '\\node[anchor=west,inner sep=3.5pt] at (%.2f,%.2f) {\\footnotesize %s};\n' % (
                    dot[0], dot[1], dotlab)
            else:          # 曲線が $a$ 軸のすぐ下を這うので，軸の上に出して引き出し線でつなぐ
                s += '\\draw[line width=0.35pt] (%.2f,%.2f) -- (2.55,0.95);\n' % dot
                s += '\\node[anchor=west,inner sep=2.5pt] at (2.45,1.15) {\\footnotesize %s};\n' % dotlab
    # カーブの呼び名
    if f > 0:
        s += '\\node[anchor=west] at (2.75,3.15) {\\footnotesize 倒立カーブ};\n'
        s += '\\node[anchor=east] at (-0.45,1.85) {\\footnotesize 正立カーブ};\n'
        s += '\\node[anchor=south] at (1.5,%.2f) {凸レンズ（$f>0$）};\n' % (bhi + 0.35)
    else:
        s += '\\node[anchor=west] at (1.85,-2.35) {\\footnotesize 正立カーブ};\n'
        s += '\\node[anchor=east] at (-1.75,-3.35) {\\footnotesize 倒立カーブ};\n'
        s += '\\node[anchor=south] at (0.0,%.2f) {凹レンズ（$f<0$）};\n' % (bhi + 0.35)
    s += '\\end{scope}\n'
    return s


# ---------------------------------------------------------------------------
#  練習［66］の解答図（球面での屈折）
#    原本（prob2_p85）の図は「どの線が法線か」が書かれておらず図だけでは読めないので，
#    ラベル付きで描き直した（2026-09-20）。
def a66():
    """点 A のまわりの拡大図。原本（prob2_p85）の図は「どの線が法線か」が
       書かれておらず図だけでは読めないので，ラベル付きで描き直した（2026-09-20）。
       角度は theta=18度, theta+phi=27度（＝n が約1.5）にとってある。"""
    import math
    th, ref, R = 18.0, 27.0, 5.0
    c = lambda d: math.cos(math.radians(d))
    sn = lambda d: math.sin(math.radians(d))
    Ox, Oy = -R * c(th), -R * sn(th)          # 球の中心 O（図の外）
    s = '\\begin{scope}[x=0.78cm,y=0.78cm]\n'
    # 球面（A を通る短い弧）とガラスの内部
    arc = [(Ox + R * c(a), Oy + R * sn(a)) for a in [2 + 34 * i / 40.0 for i in range(41)]]
    s += '\\fill[black!8] %s -- (-2.35,%.3f) -- (-2.35,%.3f) -- cycle;\n' % (
        ' -- '.join('(%.3f,%.3f)' % q for q in arc), arc[-1][1], arc[0][1])
    s += '\\draw[ln] plot[smooth] coordinates {%s};\n' % ' '.join('(%.3f,%.3f)' % q for q in arc)
    s += '\\node[anchor=north west,inner sep=1pt] at (-2.30,1.30) {\\scriptsize ガラス};\n'
    s += '\\node[anchor=south west,inner sep=2pt] at (-0.42,1.30) {\\footnotesize レンズの球面};\n'
    # 入射光（光軸に平行）
    s += '\\draw[ray] (-3.35,0) -- (0,0);\n'
    s += '\\node[anchor=south,inner sep=3pt] at (-1.85,0) {\\footnotesize 入射光（光軸に平行）};\n'
    # 法線（直線 OA）
    s += '\\draw[ext] (%.3f,%.3f) -- (%.3f,%.3f);\n' % (-2.95 * c(th), -2.95 * sn(th),
                                                        1.52 * c(th), 1.52 * sn(th))
    s += '\\node[anchor=north,inner sep=2.5pt] at (%.3f,%.3f) {\\footnotesize $\\mathrm{O}$へ};\n' \
         % (-2.45 * c(th), -2.45 * sn(th))
    s += '\\node[anchor=south west,inner sep=2pt] at (%.3f,%.3f) {\\footnotesize 法線（直線$\\mathrm{OA}$）};\n' \
         % (1.30 * c(th), 1.30 * sn(th))
    # 屈折光
    d = th - ref
    s += '\\draw[ray] (0,0) -- (%.3f,%.3f);\n' % (3.55 * c(d), 3.55 * sn(d))
    s += '\\node[anchor=north,inner sep=3pt] at (%.3f,%.3f) {\\footnotesize 屈折光};\n' % (
        2.75 * c(d), 2.75 * sn(d))
    # 角の弧
    s += '\\draw[line width=0.4pt] (%.1f:1.60) arc (%.1f:180:1.60);\n' % (180 + th, 180 + th)
    s += '\\node at (%.1f:1.95) {$\\theta$};\n' % (180 + th / 2)
    s += '\\draw[line width=0.4pt] (%.1f:1.15) arc (%.1f:%.1f:1.15);\n' % (th, th, d)
    s += '\\node[anchor=west,inner sep=1.5pt] at (%.1f:1.30) {$\\theta+\\varphi$};\n' % (th - ref / 2)
    # 点 A
    s += '\\fill (0,0) circle (1.7pt);\n'
    s += '\\node[anchor=south west,inner sep=3.5pt] at (0,0) {$\\mathrm{A}$};\n'
    s += '\\end{scope}\n'
    return s


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
    remake_xbb(out)
    print('  %-24s %6.1f KB' % (os.path.basename(out), os.path.getsize(out) / 1000))





# ---------------------------------------------------------------------------
# 穴埋め版の補助図（＝作図する前の図）を作る。
#   \AnaFig は「完全版」と「補助図」を同じ width で貼るので，**縦横比が違うと
#   高さが変わって完全版と穴埋め版のページ送りがずれる**（組版チェックリスト 4.5）。
#   ここでは問題の図を白い余白で囲んで，解答図と縦横比を一致させる。
def pad_to(src, ref, out):
    """src を ref と同じ縦横比になるまで白で囲む（中央寄せ）。"""
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from pngcrop_local import load_gray, save_gray
    w, h, g = load_gray(src)
    rw, rh, _ = load_gray(ref)
    A = rw / rh
    nw, nh = w, h
    if w / h > A:
        nh = int(round(w / A))
    else:
        nw = int(round(h * A))
    ox, oy = (nw - w) // 2, (nh - h) // 2
    c = bytearray(b'\xff' * (nw * nh))
    for y in range(h):
        c[(oy + y) * nw + ox:(oy + y) * nw + ox + w] = g[y * w:(y + 1) * w]
    save_gray(out, nw, nh, c)
    subprocess.run(['extractbb', out], capture_output=True)
    print('  %-24s %dx%d ← %s' % (os.path.basename(out), nw, nh, os.path.basename(src)))


PADS = [
 ('fig/n20_ex26.png',  'fig/n20_ex26_ans1.png', 'fig/n20_ex26_blank1.png'),
 ('fig/n20_ex26.png',  'fig/n20_ex26_ans2.png', 'fig/n20_ex26_blank2.png'),
 ('fig/n20_ex27.png',  'fig/n20_ex27_ans1.png', 'fig/n20_ex27_blank1.png'),
 ('fig/n20_ex27.png',  'fig/n20_ex27_ans2.png', 'fig/n20_ex27_blank2.png'),
 ('fig/n20_ex28a.png', 'fig/n20_ex28_ans1.png', 'fig/n20_ex28_blank1.png'),
 ('fig/n20_ex28b.png', 'fig/n20_ex28_ans2.png', 'fig/n20_ex28_blank2.png'),
 ('fig/n20_ex29a.png', 'fig/n20_ex29_ans1.png', 'fig/n20_ex29_blank1.png'),
 ('fig/n20_ex29b.png', 'fig/n20_ex29_ans2.png', 'fig/n20_ex29_blank2.png'),
]


FIGS_JA = {
 'n20_hyp_conv':  hyperbola(+1.0),
 'n20_hyp_conc':  hyperbola(-1.0),
 'n20_ex30_conv': hyperbola(+1.0, dot=(1.25,  5.00), dotlab='$(10,\\,40)$'),
 'n20_ex30_conc': hyperbola(-1.0, dot=(1.50, -0.60), dotlab='$(6.0,\\,-2.4)$'),
 # 穴埋め版：● の座標だけ伏せる（縦横比は完全版と同じ）
 'n20_ex30_conv_blank': hyperbola(+1.0, dot=(1.25,  5.00), dotlab='$(10,\\,40)$', blank=True),
 'n20_ex30_conc_blank': hyperbola(-1.0, dot=(1.50, -0.60), dotlab='$(6.0,\\,-2.4)$', blank=True),
 'n20_a66_zu':    a66(),
}


if __name__ == '__main__':
    os.chdir('/Users/yutaka/Documents/入試物理基礎演習')
    only = sys.argv[1:] or None
    for n, b in FIGS.items():
        if only and not any(k in n for k in only): continue
        build(n, b)
    for n, b in FIGS_JA.items():
        if only and not any(k in n for k in only): continue
        build_ja(n, b)
    for src, ref, out in PADS:
        if only and not any(k in out for k in only): continue
        if os.path.exists(src) and os.path.exists(ref):
            pad_to(src, ref, out)

# -*- coding: utf-8 -*-
# 新第15回の例題の「解答図」をTikZで自作する。
# 原本の例題には解答が載っていないため解答図も存在しない（組版チェックリスト 2. の方針）。
# pdflatex を使うので図中に日本語は書けない。ラベルはすべて数式記号にしてある。
import subprocess, os, math
TMPD = ('/private/tmp/claude-501/-Users-yutaka-Documents-Claude-Code----math-tex-tool/'
        '4ba70005-ebf6-4cd3-8d81-0c9c17dd53f3/scratchpad/tikz15')
os.makedirs(TMPD, exist_ok=True)

HEAD = r'''\documentclass[border=3pt]{standalone}
\usepackage{amsmath}
\usepackage{tikz}
\usetikzlibrary{arrows.meta}
\begin{document}
\begin{tikzpicture}[x=0.30cm,y=0.30cm,line join=round,
   ax/.style={-{Latex[length=2mm]},line width=0.5pt},
   cv/.style={line width=1.1pt},
   thin/.style={line width=0.35pt},
   inc/.style={line width=0.5pt},
   ref/.style={line width=0.5pt,densely dashed},
   nd/.style={line width=1.0pt,densely dashed},
   gd/.style={line width=0.3pt,densely dashed}]
'''
TAIL = r'''\end{tikzpicture}
\end{document}
'''
FIGS = {}

# ===== 例題6 水面波の干渉：腹線・節線 =========================================
# 波源 S1(-5,0), S2(5,0)．d = 10 = 2.5λ なので λ = 4．
# 原本の図に合わせて S1 は谷（山の円が r=(k+1/2)λ），S2 は山（山の円が r=kλ）＝逆位相．
lam, c = 4.0, 5.0
XMAX, YMAX = 15.0, 10.5
def hyp(a):
    """|r1-r2| = 2a の双曲線（両枝）を折れ線座標で返す"""
    b = math.sqrt(c*c - a*a)
    out = []
    for sgn in (1, -1):
        pts = []
        t = -3.0
        while t <= 3.0001:
            x = sgn * a * math.cosh(t); y = b * math.sinh(t)
            if abs(x) <= XMAX and abs(y) <= YMAX: pts.append((x, y))
            t += 0.02
        if len(pts) > 1: out.append(pts)
    return out
def path(pts, style, hide=False):
    # hide=True なら \path（描かれないがバウンディングボックスは同じ）にする。
    # 穴埋め版の図は「答えの線だけ消して寸法は完全版と同じ」でなければ
    # ページ送りがずれるので，\draw を \path に替えるだけにしてある。
    cmd = '\\path' if hide else '\\draw'
    return '%s[%s] %s;\n' % (cmd, style, ' -- '.join('(%.2f,%.2f)' % p for p in pts))

def ex6(hide=False):
  _b = ''
  # 山（実線）・谷（点線）の円：薄く描く
  for r in (2, 6, 10, 14):
      _b += '\\draw[thin] (-5,0) circle (%g);\n' % r          # S1 の山
  for r in (4, 8, 12):
      _b += '\\draw[gd] (-5,0) circle (%g);\n' % r            # S1 の谷
  for r in (4, 8, 12):
      _b += '\\draw[thin] (5,0) circle (%g);\n' % r           # S2 の山
  for r in (2, 6, 10, 14):
      _b += '\\draw[gd] (5,0) circle (%g);\n' % r             # S2 の谷
  # 腹線（強め合い）：|r1-r2| = 0.5λ, 1.5λ  → a = 1, 3　＋ 線分の外側の直線部分
  for a in (1.0, 3.0):
      for pts in hyp(a): _b += path(pts, 'cv', hide)
  _b += path([(-15,0),(-5,0)],'cv',hide) + path([(5,0),(15,0)],'cv',hide)
  # 節線（弱め合い）：|r1-r2| = 0, λ, 2λ → a = 0, 2, 4
  _b += path([(0,-10.5),(0,10.5)],'nd',hide)
  for a in (2.0, 4.0):
      for pts in hyp(a): _b += path(pts, 'nd', hide)
  _b += '\\fill (-5,0) circle (2.4pt); \\fill (5,0) circle (2.4pt);\n'
  _b += '\\node[below left=0pt,fill=white,inner sep=1pt] at (-5,0) {$\\mathrm{S_1}$};\n'
  _b += '\\node[below right=0pt,fill=white,inner sep=1pt] at (5,0) {$\\mathrm{S_2}$};\n'
  return _b

FIGS['n15_ex6_ans']   = ex6(False)
FIGS['n15_ex6_ans_blank'] = ex6(True)


# ===== 例題8 自由端反射・固定端反射の作図 =====================================
# v=2[m/s]，反射壁 x=9，入射波 y=2sin(2*pi*x/8)（λ=8, A=2）
def wave(f, x0, x1, style, hide=False, n=240):
    pts = []
    for i in range(n + 1):
        x = x0 + (x1 - x0) * i / n
        pts.append((x, f(x)))
    return path(pts, style, hide)
inc  = lambda x: 2 * math.sin(math.pi * x / 4)
free = lambda x: 2 * math.sin(math.pi * (18 - x) / 4)
fix  = lambda x: -2 * math.sin(math.pi * (18 - x) / 4)
def bg():
    """方眼（1[m]ごとの縦線・振幅の横線）と壁"""
    s = ''
    for k in range(-2, 10):
        s += '\\draw[gd] (%d,-4.0)--(%d,4.0);\n' % (k, k)
    for yv in (2, -2):
        # 目盛ラベルを右端に置くので，この2本だけ少し右まで伸ばす（2026-09-14）
        s += '\\draw[gd] (-2.6,%d)--(10.7,%d);\n' % (yv, yv)
    for yv in (2.83, -2.83):
        s += '\\draw[gd] (-2.6,%.2f)--(10.6,%.2f);\n' % (yv, yv)
    s += '\\fill[gray!35] (9,-4.2) rectangle (10.4,4.2);\n'
    s += '\\draw[line width=0.8pt] (9,-4.2)--(9,4.2);\n'
    return s

def fg():
    """軸とラベル（曲線の上に白抜きで置く）"""
    s  = '\\draw[ax] (-3,0)--(12.2,0) node[below right=-1pt]{$x$};\n'
    s += '\\draw[ax] (0,-4.4)--(0,4.4) node[above right=-2pt]{$y$};\n'
    # ラベルの重なりの修正（2026-09-14 ユーザー指摘）。旧版は
    #   ・$2$ と $2\\sqrt{2}$（および $-2$ と $-2\\sqrt{2}$）が左端の同じ列にあり，
    #     縦の間隔が 0.83 単位＝2.5mm しかないので文字どうしが潰れていた
    #   ・$8$ と $9$ が斜めに接触していた
    #   ・原点の O が below left=-1pt のせいで y 軸の右側へずれていた
    # 縦横は等倍（x=y=0.30cm）で波形を歪ませたくないので，目盛の間隔は変えずに
    # 「入射波の振幅 $\\pm2$ を右端へ，合成波の振幅 $\\pm2\\sqrt{2}$ を左端へ」と左右に分けた。
    s += '\\node[below left=1pt,fill=white,inner sep=1pt] at (0,0) {$\\mathrm{O}$};\n'
    s += '\\node[right,fill=white,inner sep=1pt] at (10.7,2) {$2$};\n'
    s += '\\node[right,fill=white,inner sep=1pt] at (10.7,-2) {$-2$};\n'
    s += '\\node[left,fill=white,inner sep=1pt] at (-2.25,2.83) {$2\\sqrt{2}$};\n'
    s += '\\node[left,fill=white,inner sep=1pt] at (-2.25,-2.83) {$-2\\sqrt{2}$};\n'
    for k in (2, 4, 6, 8):
        s += '\\node[below,fill=white,inner sep=1pt] at (%d,-0.15) {$%d$};\n' % (k, k)
    # 9 は壁の右側（グレー帯の上）へ出して 8 と離す
    s += '\\node[below right=1pt,inner sep=1pt] at (9,-0.10) {$9$};\n'
    return s

# 穴埋め版（hide=True）は入射波だけを残し，反射波と合成波は \path にして
# 「答えを描き込む前の方眼」にする。バウンディングボックスは完全版と同じ。
def ex8(refl, comp, hide=False):
    return (bg()
        + wave(inc, -2.0, 9, 'inc')
        + wave(refl, -2.0, 9, 'ref', hide)
        + wave(comp, -2.0, 9, 'cv', hide)
        + fg())
_free_c = lambda x: 2*math.sqrt(2)*math.cos(math.pi*(x-9)/4)
_fix_c  = lambda x: 2*math.sqrt(2)*math.sin(math.pi*(x-9)/4)
FIGS['n15_ex8_ans1']   = ex8(free, _free_c, False)
FIGS['n15_ex8_ans2']   = ex8(fix,  _fix_c,  False)
FIGS['n15_ex8_ans1_blank'] = ex8(free, _free_c, True)
FIGS['n15_ex8_ans2_blank'] = ex8(fix,  _fix_c,  True)

# --------------------------------------------------------------------------
def build(name, body):
    tex = os.path.join(TMPD, name + '.tex')
    open(tex, 'w', encoding='utf-8').write(HEAD + body + TAIL)
    r = subprocess.run(['pdflatex', '-interaction=nonstopmode', '-output-directory', TMPD, tex],
                       capture_output=True, text=True)
    pdf = os.path.join(TMPD, name + '.pdf')
    if not os.path.exists(pdf):
        print('  !! コンパイル失敗', name)
        print('\n'.join(l for l in r.stdout.splitlines() if l.startswith('!'))[:600]); return
    out = 'fig/%s.png' % name
    subprocess.run(['gs', '-sDEVICE=pnggray', '-r600', '-dNOPAUSE', '-dBATCH', '-o', out, pdf],
                   capture_output=True)
    subprocess.run(['extractbb', out], capture_output=True)
    print('  %-22s %6.1f KB' % (os.path.basename(out), os.path.getsize(out) / 1000))

if __name__ == '__main__':
    os.chdir('/Users/yutaka/Documents/入試物理基礎演習')
    for n, b in FIGS.items(): build(n, b)

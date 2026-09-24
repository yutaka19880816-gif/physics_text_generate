# -*- coding: utf-8 -*-
# 新第24回の例題の解答の図を TikZ で自作する。
#   原本の例題には解答が載っていない（問題枠・指針・KEY だけ）ので，作図問題の答えは自作する。
#
#     n24_ex1_ans        … 例題1(2) C が受けるクーロン力の合成（力の作用図）
#     n24_ex3_ans1 / _blank … 例題3(1) B, C（ともに +Q）だけの電気力線
#     n24_ex3_ans2 / _blank … 例題3(2) A(−2Q), B, C の電気力線（12本すべてが A に入る）
#     n24_ex4_ans  / _blank … 例題4(1)(2) 平行板間の電気力線（実線）と等電位面（点線）
#
#   _blank は穴埋め版（\AnaFig の補助図）。**消す要素は opacity=0 にする**こと
#   （\path にすると線幅の分だけ bbox が縮み，両版のページ送りがずれる。組版チェックリスト §4.5）。
#   図中に和文を書くので uplatex → dvipdfmx → gs（mkfig_new23.py と同じ）。
#   使い方:  python3 texify_draft/mkfig_new24ans.py          （全部）
#            python3 texify_draft/mkfig_new24ans.py ex3       （名前の一部で絞る）
import os, sys, subprocess, struct

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

TMPD = ('/private/tmp/claude-501/-Users-yutaka-Documents-Claude-Code----math-tex-tool/'
        '59bca349-8945-456d-922e-8c5753c43468/scratchpad/tikz24')
os.makedirs(TMPD, exist_ok=True)

HEAD = r"""\documentclass[border=3pt,dvipdfmx]{standalone}
\usepackage{amsmath}
\usepackage{tikz}
\usetikzlibrary{arrows.meta,patterns,decorations.markings}
\begin{document}
\begin{tikzpicture}[line join=round,line cap=round,
   ax/.style={line width=0.6pt,-{Latex[length=2.2mm,width=1.8mm]}},
   fl/.style={line width=0.6pt},
   fla/.style={line width=0.6pt,
               decoration={markings,mark=at position 0.55 with
                 {\arrow{Latex[length=2.0mm,width=1.6mm]}}},postaction={decorate}},
   frc/.style={-{Latex[length=2.4mm,width=2.0mm]},line width=1.0pt},
   res/.style={-{Latex[length=3.0mm,width=2.6mm]},line width=1.6pt,
               draw=black,fill=white},
   gd/.style={line width=0.4pt,dash pattern=on 1.2pt off 1.2pt},
   eq/.style={line width=0.5pt,dash pattern=on 1.6pt off 1.6pt},
   pl/.style={line width=0.8pt,pattern=north east lines}]
"""
TAIL = "\\end{tikzpicture}\n\\end{document}\n"


def remake_xbb(png):
    xbb = png[:-4] + '.xbb'
    if os.path.exists(xbb):
        os.remove(xbb)
    subprocess.run(['extractbb', png], capture_output=True)


def build(name, body):
    tex = os.path.join(TMPD, name + '.tex')
    open(tex, 'w', encoding='utf-8').write(HEAD + body + TAIL)
    r = None
    for _ in range(2):                      # 和文なので uplatex を2回
        r = subprocess.run(['uplatex', '-interaction=nonstopmode',
                            '-output-directory', TMPD, tex],
                           capture_output=True, text=True)
    dvi = os.path.join(TMPD, name + '.dvi')
    if not os.path.exists(dvi):
        print('  !! コンパイル失敗', name)
        print('\n'.join(l for l in r.stdout.splitlines() if l.startswith('!'))[:1500])
        return
    pdf = os.path.join(TMPD, name + '.pdf')
    subprocess.run(['dvipdfmx', '-o', pdf, dvi], capture_output=True)
    out = 'fig/%s.png' % name
    subprocess.run(['gs', '-sDEVICE=pnggray', '-r600', '-dNOPAUSE', '-dBATCH', '-o', out, pdf],
                   capture_output=True)
    remake_xbb(out)
    w, h = struct.unpack('>II', open(out, 'rb').read(64)[16:24])
    print('  %-22s %5dx%-5d (縦横比 %.3f)  %6.1f KB'
          % (os.path.basename(out), w, h, h / w, os.path.getsize(out) / 1000))
    return h / w


FIGS = {}

# =====================================================================
#  例題1(2)：C が A, B から受けるクーロン力の合成
#    A(-1.1,0) B(1.1,0) C(0,1.1)。CA・CB はいずれも y 軸と 45 度をなす。
# =====================================================================
FIGS['n24_ex1_ans'] = r"""
\draw[ax] (-1.85,0) -- (2.05,0); \node[below] at (1.95,-0.02) {$x$};
\draw[ax] (0,-0.55) -- (0,2.10); \node[right] at (0.04,2.02) {$y$};
\node[below left] at (0,0) {$\mathrm{O}$};
\draw[gd] (0,1.1) -- (-1.1,0);  \draw[gd] (0,1.1) -- (1.1,0);
\fill (-1.1,0) circle (2.0pt); \fill (1.1,0) circle (2.0pt); \fill (0,1.1) circle (2.0pt);
\node[below left]  at (-1.12,-0.04) {$\mathrm{A}$};
\node[below right] at (1.12,-0.04) {$\mathrm{B}$};
\node[above left]  at (-0.04,1.16) {$\mathrm{C}$};
\node[below] at (-1.1,-0.42) {$+q$}; \node[below] at (1.1,-0.42) {$+q$};
\node[above right] at (0.10,1.20) {$-q$};
% C が受ける2つの引力（CA 向き・CB 向き）
\draw[frc] (0,1.1) -- ++(225:0.80); \node[below left]  at (-0.60,0.58) {$f$};
\draw[frc] (0,1.1) -- ++(315:0.80); \node[below right] at (0.60,0.58) {$f$};
% 合力（下向き）。2本の $f$ の矢先の間に入るので，ラベルは軸のすぐ右へ白抜きで置く
\draw[res] (0,1.1) -- (0,0.02);
\node[left,fill=white,inner sep=1pt] at (-0.06,0.28) {$f_{\mathrm{C}}$};
"""

# =====================================================================
#  例題3(1)：B, C（ともに +Q）だけの電気力線。6本ずつ計12本がすべて無限遠へ。
#    B(1.15,0.85) C(1.15,-0.85)。上下対称・左右は非対称（A は無い）。
# =====================================================================
def ex3_1(show):
    o = '' if show else ',opacity=0'
    L = []
    # B から出る6本（0/60/120/180/240/300 度）。下向きの2本は C に反発して外へ逃げる。
    B = (1.15, 0.85)
    L.append(r"\draw[fla%s] (1.15,0.85) .. controls (2.6,1.0) .. (3.95,1.15);" % o)      # 0
    L.append(r"\draw[fla%s] (1.15,0.85) .. controls (2.0,1.9) .. (2.95,2.75);" % o)      # 60
    L.append(r"\draw[fla%s] (1.15,0.85) .. controls (0.3,1.9) .. (-0.65,2.75);" % o)     # 120
    L.append(r"\draw[fla%s] (1.15,0.85) .. controls (-0.3,1.0) .. (-1.65,1.15);" % o)    # 180
    L.append(r"\draw[fla%s] (1.15,0.85) .. controls (0.55,-0.18) and (-0.5,0.25) .. (-1.55,0.30);" % o)  # 240
    L.append(r"\draw[fla%s] (1.15,0.85) .. controls (1.75,-0.18) and (2.8,0.25) .. (3.85,0.30);" % o)    # 300
    # C から出る6本（B の上下反転）
    L.append(r"\draw[fla%s] (1.15,-0.85) .. controls (2.6,-1.0) .. (3.95,-1.15);" % o)
    L.append(r"\draw[fla%s] (1.15,-0.85) .. controls (2.0,-1.9) .. (2.95,-2.75);" % o)
    L.append(r"\draw[fla%s] (1.15,-0.85) .. controls (0.3,-1.9) .. (-0.65,-2.75);" % o)
    L.append(r"\draw[fla%s] (1.15,-0.85) .. controls (-0.3,-1.0) .. (-1.65,-1.15);" % o)
    L.append(r"\draw[fla%s] (1.15,-0.85) .. controls (0.55,0.18) and (-0.5,-0.25) .. (-1.55,-0.30);" % o)
    L.append(r"\draw[fla%s] (1.15,-0.85) .. controls (1.75,0.18) and (2.8,-0.25) .. (3.85,-0.30);" % o)
    head = r"""
\draw[ax] (-1.9,0) -- (4.15,0); \node[below] at (4.05,-0.04) {$x$};
\draw[ax] (0,-2.95) -- (0,2.95); \node[right] at (0.05,2.88) {$y$};
\fill (1.15,0.85) circle (2.2pt); \fill (1.15,-0.85) circle (2.2pt);
\node[above right] at (1.20,0.92) {$\mathrm{B}\ (+Q)$};
\node[below right] at (1.20,-0.92) {$\mathrm{C}\ (+Q)$};
"""
    m = '' if show else '[opacity=0]'
    tail = (r"\fill%s (1.15,0) circle (1.5pt);" % m) + "\n" \
         + (r"\node[below%s,fill=white,inner sep=1pt] at (1.15,-0.06) {\footnotesize 電場 $0$};"
            % (',opacity=0' if not show else ''))
    return head + '\n'.join(L) + '\n' + tail + '\n'

FIGS['n24_ex3_ans1']       = ex3_1(True)
FIGS['n24_ex3_ans1_blank'] = ex3_1(False)

# =====================================================================
#  例題3(2)：A(−2Q) を加えると B, C から出た12本すべてが A に入る。
# =====================================================================
def ex3_2(show):
    o = '' if show else ',opacity=0'
    # B(1.15,0.85) から出る6本がすべて A(0,0) に入る。
    #   4本は B→A の弧（BA の中点から垂直に t だけずらした点を制御点にする）。
    #   残り2本は「A と反対向きに出た電気力線も回り込んで A に入る」ことを示すため大きく回す。
    #   t を上半面側だけにとるのは，下半面は C から出た6本の領域で，交わってはいけないため。
    ARC = [-0.30, 0.05, 0.40, 0.85]
    MX, MY = 0.575, 0.425                 # BA の中点
    PX, PY = -0.594, 0.804                # BA に垂直な単位ベクトル（上側）
    WRAP = [((1.75, 2.25), (-1.10, 1.55)),   # 上へ出て 125 度から入る
            ((3.25, 1.55), (-2.20, 0.95))]   # 右へ出て 157 度から大きく回り込む
    L = []
    for c in (1, -1):                     # c=+1 が B，c=-1 が C（上下対称）
        for t in ARC:
            cx, cy = MX + t * PX, (MY + t * PY) * c
            L.append(r"\draw[fla%s] (1.15,%.2f) .. controls (%.3f,%.3f) .. (0,0);"
                     % (o, 0.85 * c, cx, cy))
        for (p1, p2) in WRAP:
            L.append(r"\draw[fla%s] (1.15,%.2f) .. controls (%.2f,%.2f) and (%.2f,%.2f) .. (0,0);"
                     % (o, 0.85 * c, p1[0], p1[1] * c, p2[0], p2[1] * c))
    head = r"""
\draw[ax] (-2.30,0) -- (3.55,0); \node[below] at (3.45,-0.04) {$x$};
\draw[ax] (0,-2.35) -- (0,2.35); \node[right] at (0.05,2.28) {$y$};
\fill (0,0) circle (2.6pt);
\fill (1.15,0.85) circle (2.2pt); \fill (1.15,-0.85) circle (2.2pt);
\node[left,fill=white,inner sep=1pt]  at (-0.55,-0.30) {$\mathrm{A}\ (-2Q)$};
\node[above right,fill=white,inner sep=1pt] at (1.24,0.94) {$\mathrm{B}\ (+Q)$};
\node[below right,fill=white,inner sep=1pt] at (1.24,-0.94) {$\mathrm{C}\ (+Q)$};
"""
    note = (r"\node[fill=white,inner sep=1.5pt%s] at (1.75,-2.05) "
            r"{\footnotesize 12本すべてが $\mathrm{A}$ に入る};" % o)
    return head + '\n'.join(L) + '\n' + note + '\n'

FIGS['n24_ex3_ans2']       = ex3_2(True)
FIGS['n24_ex3_ans2_blank'] = ex3_2(False)

# =====================================================================
#  例題4(1)(2)：平行板間の電気力線（実線・下向き）と等電位面（点線・水平）
# =====================================================================
def ex4(show):
    o = '' if show else ',opacity=0'
    L = []
    for x in [0.55, 1.65, 2.75, 3.85, 4.95, 6.05, 7.15]:
        L.append(r"\draw[fl%s,-{Latex[length=2.2mm,width=1.8mm]}] (%.2f,3.00) -- (%.2f,0.28);"
                 % (o, x, x))
    for y, lab in [(2.25, r'$\frac{3}{4}V$'), (1.50, r'$\frac{1}{2}V$'), (0.75, r'$\frac{1}{4}V$')]:
        L.append(r"\draw[eq%s] (0.20,%.2f) -- (7.50,%.2f);" % (o, y, y))
        L.append(r"\node[left%s] at (0.16,%.2f) {\footnotesize %s};" % (o, y, lab))
    head = r"""
\fill[pattern=north east lines] (0.20,3.05) rectangle (7.50,3.35);
\draw[line width=0.8pt] (0.20,3.05) rectangle (7.50,3.35);
\fill[pattern=north east lines] (0.20,-0.30) rectangle (7.50,0.00);
\draw[line width=0.8pt] (0.20,-0.30) rectangle (7.50,0.00);
\node[right] at (7.58,3.20) {$\mathrm{X}$};
\node[right] at (7.58,-0.15) {$\mathrm{Y}$};
\node[left] at (0.16,3.20) {\footnotesize $V$};
\node[left] at (0.16,-0.15) {\footnotesize $0$};
"""
    return head + '\n'.join(L) + '\n'

FIGS['n24_ex4_ans']       = ex4(True)
FIGS['n24_ex4_ans_blank'] = ex4(False)


if __name__ == '__main__':
    os.chdir('/Users/yutaka/Documents/入試物理基礎演習')
    only = sys.argv[1:] or None
    ratios = {}
    for name in sorted(FIGS):
        if only and not any(k in name for k in only):
            continue
        ratios[name] = build(name, FIGS[name])
    # 完全版と補助図の縦横比が一致しているか（ずれると両版のページ送りが狂う）
    for n in sorted(ratios):
        if n.endswith('_blank'):
            base = n[:-6]
            if base in ratios and ratios[base] and ratios[n]:
                d = abs(ratios[base] - ratios[n])
                print('  縦横比チェック %-18s %s (差 %.4f)'
                      % (base, 'OK' if d < 0.003 else '!! ずれている', d))

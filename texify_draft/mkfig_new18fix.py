# -*- coding: utf-8 -*-
# 2026-09-14 第18回の図の作り直し（ユーザー指摘の反映）
#   n18_mirror_rot … 18.2「鏡をθ回すと反射光は2θ振れる」。旧版は法線が無く，回転後の鏡が
#                    細い破線で3本目の光線に見えていたので，鏡M/M'・法線N/N'・反射光R/R'を
#                    すべて描き分けて，θ（鏡どうし）・θ（法線どうし）・2θ（反射光どうし）を示す。
#   ch18_ex19_ans  … 例題22(2) 斜め入射の回折格子。旧版は例題の図（原本スキャン
#                    ch25_ex22_grating.png）と左右が反転していたので，例題に合わせて
#                    「入射光は右下から来て左上へ回折する（θ, θ0 はともに反時計回り＝左側）」に直した。
#
# pdflatex + standalone なので図中に日本語は書けない（ラベルはすべて記号）。
# 出力は fig/*.png（600dpi グレースケール）＋ extractbb で .xbb。
import subprocess, os, sys, math

TMPD = ('/private/tmp/claude-501/-Users-yutaka-Documents-Claude-Code----math-tex-tool/'
        '4ba70005-ebf6-4cd3-8d81-0c9c17dd53f3/scratchpad/tikz_new18fix')
os.makedirs(TMPD, exist_ok=True)

HEAD = r'''\documentclass[border=3pt]{standalone}
\usepackage{amsmath}
\usepackage{tikz}
\usetikzlibrary{arrows.meta,patterns}
\begin{document}
\begin{tikzpicture}[line join=round,
   wall/.style={line width=1.1pt},
   ray/.style={-{Latex[length=2.0mm]},line width=0.9pt},
   thick ray/.style={-{Latex[length=2.2mm]},line width=1.6pt},
   plain/.style={line width=0.9pt},
   wf/.style={line width=0.5pt},
   nrm/.style={line width=0.5pt,densely dashed},
   ext/.style={line width=0.5pt,densely dashed},
   arc/.style={line width=0.5pt},
   arcA/.style={-{Latex[length=1.4mm]},line width=0.5pt},
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


def pol(r, adeg):
    return (r * math.cos(math.radians(adeg)), r * math.sin(math.radians(adeg)))


# ---------------------------------------------------------------------------
# 18.2 鏡を θ 回すと反射光は 2θ 振れる。入射光は固定。
#   M(実線＋ハッチ)→M'(実線) / N(破線)→N'(破線) / R→R' の3組を描き分ける。
#   角度の取り方：鏡 M を 0°，法線 N を 90° とし，鏡を反時計回りに θ 回す。
#   入射角 i は法線から測る。回転前の反射光は 90-i，回転後は 90-i+2θ の向き。
def fig_mirror_rot():
    th, i = 30.0, 46.0
    Lm, Lmp, Lr, Ln = 2.35, 1.95, 2.60, 1.55
    aIn, aR, aRp = 90 + i, 90 - i, 90 - i + 2 * th          # 136, 44, 104
    aN, aNp, aM, aMp = 90.0, 90 + th, 0.0, th               # 90, 120, 0, 30

    s = ''
    # 鏡 M（回転前）＝実線＋ハッチ
    s += '\\draw[wall] (%.3f,0) -- (%.3f,0);\n' % (-Lm, Lm)
    s += hatch(-Lm, Lm, 0.0, n=13, dx=0.20, dy=-0.24)
    # 鏡 M'（回転後）＝実線。左半分は M のハッチと交差して読みにくいので右半分だけ描く
    s += '\\draw[wall] (0,0) -- (%.3f,%.3f);\n' % pol(Lmp, aMp)
    # 法線 N, N'
    s += '\\draw[nrm] (0,0) -- (%.3f,%.3f);\n' % pol(Ln, aN)
    s += '\\draw[nrm] (0,0) -- (%.3f,%.3f);\n' % pol(Ln, aNp)
    # 入射光（固定）
    s += '\\draw[ray] (%.3f,%.3f) -- (%.3f,%.3f);\n' % (pol(Lr, aIn) + pol(0.55, aIn))
    s += '\\draw[plain] (%.3f,%.3f) -- (0,0);\n' % pol(0.55, aIn)
    # 反射光 R（回転前）・R'（回転後）
    s += '\\draw[ray] (0,0) -- (%.3f,%.3f);\n' % pol(Lr, aR)
    s += '\\draw[ray] (0,0) -- (%.3f,%.3f);\n' % pol(Lr, aRp)
    # 角度：θ（鏡どうし）・θ（法線どうし）・2θ（反射光どうし）
    s += '\\draw[arc] (%.3f,%.3f) arc (%.1f:%.1f:1.30);\n' % (pol(1.30, aM) + (aM, aMp))
    s += '\\node[lb] at (%.3f,%.3f) {\\footnotesize $\\theta$};\n' % pol(1.56, (aM + aMp) / 2)
    s += '\\draw[arc] (%.3f,%.3f) arc (%.1f:%.1f:0.80);\n' % (pol(0.80, aN) + (aN, aNp))
    s += '\\node[lb] at (%.3f,%.3f) {\\footnotesize $\\theta$};\n' % pol(0.98, (aN + aNp) / 2)
    s += '\\draw[arc] (%.3f,%.3f) arc (%.1f:%.1f:2.15);\n' % (pol(2.15, aR) + (aR, aRp))
    s += '\\node[lb] at (%.3f,%.3f) {\\footnotesize $2\\theta$};\n' % pol(2.40, (aR + aRp) / 2)
    # ラベル
    s += '\\node[lb] at (%.3f,%.3f) {\\footnotesize $\\mathrm{M}$};\n' % (Lm + 0.20, 0.17)
    s += '\\node[lb] at (%.3f,%.3f) {\\footnotesize $\\mathrm{M}^\\prime$};\n' % pol(Lmp + 0.24, aMp)
    s += '\\node[lb] at (%.3f,%.3f) {\\footnotesize $\\mathrm{N}$};\n' % pol(Ln + 0.20, aN)
    s += '\\node[lb] at (%.3f,%.3f) {\\footnotesize $\\mathrm{N}^\\prime$};\n' % pol(Ln + 0.22, aNp)
    s += '\\node[lb] at (%.3f,%.3f) {\\footnotesize $\\mathrm{R}$};\n' % pol(Lr + 0.22, aR)
    s += '\\node[lb] at (%.3f,%.3f) {\\footnotesize $\\mathrm{R}^\\prime$};\n' % pol(Lr + 0.24, aRp)
    s += '\\node[lb] at (%.3f,%.3f) {\\footnotesize $\\mathrm{O}$};\n' % (-0.24, -0.26)
    s += '\\fill (0,0) circle (1.5pt);\n'
    return s


# ---------------------------------------------------------------------------
# 例題22(2) 斜め入射の回折格子。
#   例題の図（原本）に合わせ，入射光は右下から来て左上へ抜ける。θ, θ0 はどちらも
#   格子の法線（鉛直破線）から反時計回り＝左向きに測った正の角。
#   A ＝ 先に波面が届く側（右）のスリット，B ＝ 後から届く側（左）のスリット。
#   入射側：AF ⊥ 入射光，FB ＝ d sinθ0 だけ B へ入る光が余分に進む。
#   回折側：BG ⊥ 回折光，AG ＝ d sinθ だけ A から出る光が余分に進む。
def fig_grating_oblique():
    th, th0 = 50.0, 25.0
    a = 1.15                                   # A, B の x 座標（±a），格子定数 d = 2a
    u = (-math.sin(math.radians(th)), math.cos(math.radians(th)))     # 回折光の向き
    u0 = (-math.sin(math.radians(th0)), math.cos(math.radians(th0)))  # 入射光の向き
    A, B = (a, 0.0), (-a, 0.0)
    d = 2 * a
    G = (A[0] + d * math.sin(math.radians(th)) * u[0],
         A[1] + d * math.sin(math.radians(th)) * u[1])
    F = (B[0] - d * math.sin(math.radians(th0)) * u0[0],
         B[1] - d * math.sin(math.radians(th0)) * u0[1])
    Lup, Ldn = 2.45, 2.35
    bar, gap = 2.60, 0.14

    def ptr(P, t, v):
        return (P[0] + t * v[0], P[1] + t * v[1])

    s = ''
    # 鉛直の破線（格子面の法線）
    for P in (A, B):
        s += '\\draw[ext] (%.3f,-1.55) -- (%.3f,1.95);\n' % (P[0], P[0])
    # 回折格子の板（スリットの位置だけ白く抜く）
    for x0, x1 in ((-bar, B[0] - gap), (B[0] + gap, A[0] - gap), (A[0] + gap, bar)):
        s += ('\\draw[line width=0.4pt,fill=gray!45] (%.3f,-0.14) rectangle (%.3f,0.14);\n'
              % (x0, x1))
    # 入射光（右下から左上へ）：A へ入る光と B へ入る光
    for P in (A, B):
        s += '\\draw[ray] (%.3f,%.3f) -- (%.3f,%.3f);\n' % (ptr(P, -Ldn, u0) + ptr(P, -1.05, u0))
        s += '\\draw[plain] (%.3f,%.3f) -- (%.3f,%.3f);\n' % (ptr(P, -1.05, u0) + P)
    # 回折光（左上へ）
    for P in (A, B):
        s += '\\draw[plain] (%.3f,%.3f) -- (%.3f,%.3f);\n' % (P + ptr(P, Lup, u))
    s += '\\draw[ray] (%.3f,%.3f) -- (%.3f,%.3f);\n' % (ptr(B, 1.25, u) + ptr(B, Lup, u))
    s += '\\draw[ray] (%.3f,%.3f) -- (%.3f,%.3f);\n' % (ptr(A, 1.90, u) + ptr(A, Lup, u))
    # 経路差：入射側 FB と回折側 AG を太線で強調
    s += '\\draw[thick ray] (%.3f,%.3f) -- (%.3f,%.3f);\n' % (F + B)
    s += '\\draw[thick ray] (%.3f,%.3f) -- (%.3f,%.3f);\n' % (A + G)
    # 垂線（波面）
    s += '\\draw[ext] (%.3f,%.3f) -- (%.3f,%.3f);\n' % (A + F)
    s += '\\draw[ext] (%.3f,%.3f) -- (%.3f,%.3f);\n' % (B + G)
    # 格子定数 d
    s += ('\\draw[{Latex[length=1.8mm]}-{Latex[length=1.8mm]},line width=0.5pt]'
          ' (%.3f,-0.62) -- (%.3f,-0.62);\n' % (B[0], A[0]))
    s += '\\node[lb] at (0.52,-0.62) {\\footnotesize $d$};\n'
    # 角度 θ（回折側・A の鉛直線から）と θ0（入射側・A の鉛直線から）
    s += '\\draw[arcA] (%.3f,%.3f) arc (90:%.1f:0.78);\n' % (A[0], A[1] + 0.78, 90 + th)
    s += '\\node[lb] at (%.3f,%.3f) {\\footnotesize $\\theta$};\n' % (
        A[0] + 0.98 * math.cos(math.radians(90 + th / 2)), 0.98 * math.sin(math.radians(90 + th / 2)))
    s += '\\draw[arcA] (%.3f,%.3f) arc (-90:%.1f:0.72);\n' % (A[0], A[1] - 0.72, -90 + th0)
    s += '\\node[lb] at (%.3f,%.3f) {\\footnotesize $\\theta_0$};\n' % (
        A[0] + 0.95 * math.cos(math.radians(-90 + th0 / 2)), 0.95 * math.sin(math.radians(-90 + th0 / 2)))
    # 点と文字
    for P, lab, off in ((A, '\\mathrm{A}', (0.30, 0.34)), (B, '\\mathrm{B}', (-0.34, 0.30)),
                        (G, '\\mathrm{G}', (0.10, 0.32)), (F, '\\mathrm{F}', (0.32, -0.16))):
        s += '\\fill (%.3f,%.3f) circle (1.7pt);\n' % P
        s += '\\node[lb] at (%.3f,%.3f) {\\footnotesize $%s$};\n' % (P[0] + off[0], P[1] + off[1], lab)
    # 経路差の長さのラベル
    # 経路差のラベルは三角形 ABG・ABF の内側に置く（原本の図と同じ置き方を左右反転したもの）
    s += '\\node[lb] at (-0.08,0.45) {\\footnotesize $d\\sin\\theta$};\n'
    s += '\\node[lb] at (-0.30,-0.37) {\\footnotesize $d\\sin\\theta_0$};\n'
    return s


FIGS = {
    'n18_mirror_rot': fig_mirror_rot,
    'ch18_ex19_ans':  fig_grating_oblique,
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

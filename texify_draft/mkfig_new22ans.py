# -*- coding: utf-8 -*-
# 新第22回（気体分子運動論と内部エネルギー）の解説図を TikZ で自作する。
#   旧⑮の講義（気体分子運動論・内部エネルギー・P-V図）には図が1枚も無く，
#   結論の式と「手順①〜⑥」だけが並んでいたので，つまずきやすい所に図を足した。
#     n22_zu_seibun … 22.1 速度の成分分解と等方性（v^2=vx^2+vy^2+vz^2）
#     n22_zu_ofuku  … 22.1 衝突の間隔（x方向に往復2l／τ=2l/|vx|）
#     n22_zu_bunshi … 22.2 単原子分子と二原子分子（並進だけ／並進＋回転）
#     n22_zu_teiseki… 22.4 定積加熱と定圧加熱の対比（力の作用図つき・C_P>C_V の理由）
#     n22_zu_kabe   … 練習［21］(6) 動くピストンとの弾性衝突（静止系とピストン系）
#   図中に和文を書くので uplatex → dvipdfmx → gs（mkfig_new21ans.py と同じ方式）。
#   使い方:  python3 texify_draft/mkfig_new22ans.py            （全部作り直す）
#            python3 texify_draft/mkfig_new22ans.py kabe       （名前を指定して1枚だけ）
import os, sys, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

TMPD = ('/private/tmp/claude-501/-Users-yutaka-Documents-Claude-Code----math-tex-tool/'
        '6d04a7ea-dc96-4125-889d-17dac178c6e5/scratchpad/tikz22')
os.makedirs(TMPD, exist_ok=True)

HEAD = r"""\documentclass[border=3pt,dvipdfmx]{standalone}
\usepackage{amsmath}
\usepackage{tikz}
\usetikzlibrary{arrows.meta,decorations.pathmorphing}
\begin{document}
\begin{tikzpicture}[line join=round,line cap=round,
   wall/.style={line width=1.1pt},
   thn/.style={line width=0.5pt},
   frc/.style={-{Latex[length=2.2mm,width=1.8mm]},line width=1.0pt},
   vel/.style={-{Latex[length=2.0mm,width=1.6mm]},line width=0.8pt},
   dim/.style={{Latex[length=1.6mm]}-{Latex[length=1.6mm]},line width=0.5pt},
   gd/.style={line width=0.4pt,dash pattern=on 1.2pt off 1.2pt}]
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
    for _ in range(2):                      # 和文なので uplatex を2回
        r = subprocess.run(['uplatex', '-interaction=nonstopmode', '-output-directory', TMPD, tex],
                           capture_output=True, text=True)
    dvi = os.path.join(TMPD, name + '.dvi')
    if not os.path.exists(dvi):
        print('  !! コンパイル失敗', name)
        print('\n'.join(l for l in r.stdout.splitlines() if l.startswith('!'))[:1200]); return
    pdf = os.path.join(TMPD, name + '.pdf')
    subprocess.run(['dvipdfmx', '-o', pdf, dvi], capture_output=True)
    out = 'fig/%s.png' % name
    subprocess.run(['gs', '-sDEVICE=pnggray', '-r600', '-dNOPAUSE', '-dBATCH', '-o', out, pdf],
                   capture_output=True)
    remake_xbb(out)
    import struct
    w, h = struct.unpack('>II', open(out, 'rb').read(64)[16:24])
    print('  %-24s %5dx%-5d (縦横比 %.2f)  %6.1f KB'
          % (os.path.basename(out), w, h, h / w, os.path.getsize(out) / 1000))


FIGS = {}

# ------------------------------------------------ 22.1 速度の成分分解と等方性
# x：右／y：上／z：左下（例題5の原本の図と軸の取り方を揃えた）
_vx, _vy = 3.4, 2.4
_zx, _zy = -1.364, -1.012          # vz*ez
FIGS['n22_zu_seibun'] = r"""
%% 直方体の稜（破線）。12本のうち3本は座標軸なので，残り9本をすべて描く
\draw[gd] (%(ax)s,0) -- (%(px)s,%(pz)s) -- (%(zx)s,%(zy)s);
\draw[gd] (%(ax)s,0) -- (%(ax)s,%(ay)s) -- (%(tx)s,%(ty)s) -- (%(zx)s,%(zy2)s);
\draw[gd] (0,%(ay)s) -- (%(ax)s,%(ay)s);
\draw[gd] (0,%(ay)s) -- (%(zx)s,%(zy2)s);
\draw[gd] (%(px)s,%(pz)s) -- (%(tx)s,%(ty)s);
%% 奥左の鉛直稜（2026-09-20 ユーザー指摘：ここが抜けていて直方体が閉じていなかった）
\draw[gd] (%(zx)s,%(zy)s) -- (%(zx)s,%(zy2)s);
%% 座標軸
\draw[thn,-{Latex[length=2.0mm,width=1.6mm]}] (0,0) -- (4.55,0);   \node[below] at (4.55,-0.05) {$x$};
\draw[thn,-{Latex[length=2.0mm,width=1.6mm]}] (0,0) -- (0,3.10);   \node[left]  at (-0.05,3.05) {$y$};
\draw[thn,-{Latex[length=2.0mm,width=1.6mm]}] (0,0) -- (-1.95,-1.45); \node[below] at (-1.95,-1.45) {$z$};
%% 速度ベクトルと3成分
\draw[frc] (0,0) -- (%(tx)s,%(ty)s);
\draw[vel] (0,0) -- (%(ax)s,0);
\draw[vel] (0,0) -- (0,%(ay)s);
\draw[vel] (0,0) -- (%(zx)s,%(zy)s);
%% ラベルは白抜きにして破線と重ならないようにする（組版チェックリスト §2）
\node[fill=white,inner sep=1pt,anchor=south] at (%(tx)s,%(tyv)s) {$v$};
\node[fill=white,inner sep=1pt,below] at (%(hx)s,-0.10) {$v_x$};
\node[fill=white,inner sep=1pt,right] at (0.12,0.85) {$v_y$};
\node[fill=white,inner sep=1pt,above left] at (-0.62,-0.42) {$v_z$};
\fill (0,0) circle (1.6pt);
""" % dict(ax=_vx, ay=_vy, zx=_zx, zy=_zy, zy2=_vy + _zy,
           px=_vx + _zx, pz=_zy, tx=_vx + _zx, ty=_vy + _zy,
           tyv=_vy + _zy + 0.22,
           hx=_vx / 2, hy=_vy / 2)

# ------------------------------------------------ 22.1 往復距離 2l と衝突の間隔
FIGS['n22_zu_ofuku'] = r"""
%% 容器の断面（右の壁が注目する面）
\draw[thn] (0,0) rectangle (4.6,3.0);
\draw[wall,line width=2.2pt] (4.6,0) -- (4.6,3.0);
\node[right,align=left] at (4.80,1.5) {注目\\する面};
%% 分子の軌跡（右の壁 → 左の壁 → 右の壁）
\draw[vel] (4.52,2.55) -- (0.08,1.50);
\draw[vel] (0.08,1.50) -- (4.52,0.55);
\fill (4.52,2.55) circle (2.4pt);
\fill (4.52,0.55) circle (2.4pt);
\node[left] at (4.42,2.80) {\small 衝突};
\node[left] at (4.42,0.28) {\small 再び衝突};
%% x 方向の往復
\draw[dim] (0,-0.42) -- (4.6,-0.42);
\node[below] at (2.3,-0.44) {$l$};
\draw[vel] (0.95,3.35) -- (2.25,3.35); \node[right] at (2.30,3.35) {$x$};
"""

# ------------------------------------------------ 22.2 単原子分子と二原子分子
FIGS['n22_zu_bunshi'] = r"""
%% ---- 左：単原子分子 -------------------------------------------------
\begin{scope}[shift={(0,0)}]
  \draw[vel] (0,0) -- (1.55,0);      \node[right] at (1.57,0)     {$v_x$};
  \draw[vel] (0,0) -- (0,1.40);      \node[above] at (0,1.42)     {$v_y$};
  \draw[vel] (0,0) -- (-1.00,-0.74); \node[left] at (-1.02,-0.70){$v_z$};
  \fill[gray!25] (0,0) circle (0.40);
  \draw[thn]     (0,0) circle (0.40);
  \node[anchor=north,align=center] at (0.25,-1.75)
    {単原子分子（He, Ne, Ar $\cdots$）\\[1mm] 並進運動の3方向だけ\\[2.5mm]
     $\dfrac{1}{2}m\overline{v^2}=\dfrac{3}{2}k_{\mathrm{B}}T$\quad
     $U=\dfrac{3}{2}nRT$};
\end{scope}
%% ---- 仕切り --------------------------------------------------------
\draw[gd] (3.30,1.75) -- (3.30,-3.55);
%% ---- 右：二原子分子 -------------------------------------------------
\begin{scope}[shift={(7.35,0)}]
  %% 回転を表す弧（分子のまわりを回る）
  \draw[-{Latex[length=2.0mm,width=1.6mm]},line width=0.7pt]
        (-1.15,0.62) arc (150:30:1.33);
  \draw[-{Latex[length=2.0mm,width=1.6mm]},line width=0.7pt]
        (1.15,-0.62) arc (-30:-150:1.33);
  \node[left]  at (-1.20,0.72) {回転};
  %% 亜鈴型の分子
  \draw[wall] (-0.50,-0.36) -- (0.50,0.36);
  \fill[gray!25] (-0.50,-0.36) circle (0.34); \draw[thn] (-0.50,-0.36) circle (0.34);
  \fill[gray!25] ( 0.50, 0.36) circle (0.34); \draw[thn] ( 0.50, 0.36) circle (0.34);
  %% 回転の弧は 150〜30 度と -30〜-150 度にあるので，並進はその切れ目（右）へ向ける
  \draw[vel] (0,0) -- (1.90,0);  \node[right] at (1.94,0) {並進};
  \node[anchor=north,align=center] at (0.25,-1.75)
    {二原子分子（$\mathrm{N_2}$, $\mathrm{O_2}$ $\cdots$）\\[1mm] 並進のほかに回転もする\\[2.5mm]
     回転のぶんだけ余分に蓄えられて\ \ $U=\dfrac{5}{2}nRT$};
\end{scope}
"""

# ------------------------------------------------ 22.4 定積加熱と定圧加熱

def _cyl(fixed):
    """シリンダー1本。fixed=True ならストッパーで固定（定積），False なら自由（定圧）。
       ラベルが側壁に乗らないよう内径を 3.6（0.25〜3.85）まで広げ，
       下向きの2力のラベルは矢印の真上に置いてある（2026-09-20 ユーザー指摘の重なり対策）。"""
    s = r"""
  %% 気体（塗りを先に。あとから壁を描く。先に壁を描くと塗りに隠れる）
  \fill[gray!12] (0.25,0.25) rectangle (3.85,1.80);
  %% ピストン
  \fill[gray!50] (0.25,1.80) rectangle (3.85,2.17);
  %% シリンダー（側壁と底）
  \draw[wall] (0.25,4.05) -- (0.25,0.25) -- (3.85,0.25) -- (3.85,4.05);
  \draw[wall] (0.25,1.80) rectangle (3.85,2.17);
  %% ヒーター
  \draw[thn,decorate,decoration={coil,aspect=0.6,segment length=2.6mm,amplitude=1.2mm}]
        (1.15,0.62) -- (2.95,0.62);
  \draw[frc] (2.05,-0.62) -- (2.05,0.20); \node[left] at (1.98,-0.30) {$Q$};
  %% 気体がピストンを押す力（必ず上向き）
  \draw[frc] (1.20,0.95) -- (1.20,1.77); \node[left] at (1.16,1.36) {$PS$};
"""
    if fixed:
        s += r"""
  %% ストッパー（ピストンの上に載せて動かないように押さえている）
  \fill (-0.05,2.17) rectangle (0.30,2.28);
  \fill (3.80,2.17) rectangle (4.15,2.28);
  \node[left]  at (-0.08,2.225) {\small 固定};
  \node[right] at (4.18,2.225) {\small 固定};
  %% 加熱すると P>P_0 になるので，ストッパーがピストンを下向きに押さえる
  \draw[frc] (1.05,3.58) -- (1.05,2.32);
  \node[anchor=south] at (1.05,3.62) {$P_0S$};
  \draw[frc] (2.75,3.58) -- (2.75,2.32);
  \node[anchor=south] at (2.75,3.62) {\small ストッパーの力};
"""
    else:
        s += r"""
  \draw[frc] (2.05,3.58) -- (2.05,2.32);
  \node[anchor=south] at (2.05,3.62) {$P_0S$};
  %% ピストンが上がったあとの位置（細い破線）と，その上がり幅 Δl
  \draw[gd] (0.25,2.92) -- (3.85,2.92);
  \draw[thn] (3.85,2.17) -- (4.55,2.17);
  \draw[thn] (3.85,2.92) -- (4.55,2.92);
  \draw[dim] (4.35,2.17) -- (4.35,2.92);
  \node[right] at (4.60,2.545) {$\varDelta l$};
"""
    return s

FIGS['n22_zu_teiseki'] = (r"""
%% ---------------- 左：定積変化 ----------------
\begin{scope}[shift={(0,0)}]
""" + _cyl(True) + r"""
  \node[anchor=north,align=center] at (2.05,-1.15)
    {\textbf{定積変化}（ピストンを固定）\\[1.2mm]
     体積が変わらない\ $\Rightarrow$\ $W_{\mathrm{out}}=0$\\[1.2mm]
     $Q=\varDelta U=nC_V\varDelta T$};
  %% エネルギーの配分
  \draw[thn] (0.45,-3.70) rectangle (3.15,-3.18);
  \node at (1.80,-3.44) {$\varDelta U$};
  \node[left] at (0.33,-3.44) {$Q$};
\end{scope}
%% ---------------- 右：定圧変化 ----------------
\begin{scope}[shift={(7.9,0)}]
""" + _cyl(False) + r"""
  \node[anchor=north,align=center] at (2.05,-1.15)
    {\textbf{定圧変化}（ピストンは自由）\\[1.2mm]
     $PS=P_0S$\ より\ $P=P_0$（一定）\\[1.2mm]
     $Q=\varDelta U+P\varDelta V=nC_P\varDelta T$};
  %% エネルギーの配分
  \draw[thn] (0.45,-3.70) rectangle (3.15,-3.18);
  \fill[gray!30] (3.15,-3.70) rectangle (4.50,-3.18);
  \draw[thn] (3.15,-3.70) rectangle (4.50,-3.18);
  \node at (1.80,-3.44) {$\varDelta U$};
  \node at (3.83,-3.44) {$W_{\mathrm{out}}$};
  \node[left] at (0.33,-3.44) {$Q$};
\end{scope}
""")

# ------------------------------------------------ 練習［21］(6) 動く壁との弾性衝突
FIGS['n22_zu_kabe'] = r"""
%% 解答編は2段組（段幅76mm）なので，貼付幅62mmで文字が読める大きさになるよう
%% 図全体を6cm角ほどに収める。長い説明文は図に入れず本文側に置く。
%% ---------------- 上：静止した床から見る ----------------
\begin{scope}[shift={(0,0)}]
  \node[anchor=west] at (0,2.35) {\textbf{床から見ると}};
  \fill[gray!45] (4.55,-0.05) rectangle (4.85,1.95);
  \draw[wall]    (4.55,-0.05) rectangle (4.85,1.95);
  \draw[frc] (4.45,2.28) -- (3.75,2.28); \node[left] at (3.70,2.28) {$u$};
  \node[right] at (4.95,1.00) {ピストン};
  %% 衝突前
  \fill (0.85,1.35) circle (2.2pt);
  \draw[vel] (1.05,1.35) -- (2.80,1.35); \node[above] at (1.95,1.36) {$v_x$};
  %% 衝突後
  \fill (2.80,0.40) circle (2.4pt);
  \draw[vel] (2.60,0.40) -- (0.35,0.40); \node[above] at (1.50,0.41) {$v_x+2u$};
\end{scope}
%% ---------------- 下：ピストンとともに動きながら見る ----------------
\begin{scope}[shift={(0,-3.30)}]
  \node[anchor=west] at (0,2.35) {\textbf{ピストンとともに動くと}};
  \fill[gray!45] (4.55,-0.05) rectangle (4.85,1.95);
  \draw[wall]    (4.55,-0.05) rectangle (4.85,1.95);
  \node[right,align=left] at (4.95,1.00) {静止して\\見える};
  \fill (0.85,1.35) circle (2.2pt);
  \draw[vel] (1.05,1.35) -- (2.80,1.35); \node[above] at (1.95,1.36) {$v_x+u$};
  \fill (2.80,0.40) circle (2.4pt);
  \draw[vel] (2.60,0.40) -- (0.85,0.40); \node[above] at (1.75,0.41) {$v_x+u$};
\end{scope}
"""

if __name__ == '__main__':
    os.chdir('/Users/yutaka/Documents/入試物理基礎演習')
    only = [a for a in sys.argv[1:] if not a.startswith('--')]
    for name, body in FIGS.items():
        if only and not any(o in name for o in only):
            continue
        build(name, body)

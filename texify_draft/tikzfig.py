# -*- coding: utf-8 -*-
# TikZ／circuitikz で自作図を作る共通部品（第26回以降の電磁気で使う）。
#   build(name, body) … fig/<name>.png（600dpi・グレー）を作り，.xbb を作り直す。
#   和文ラベルを書けるように uplatex ×2 → dvipdfmx → gs で組む（組版チェックリスト §1.6）。
#   作業ファイルは環境変数 TIKZ_TMP（無ければ /tmp/tikzfig）に置く。
#
#   回路図は circuitikz の european 系（抵抗＝長方形）で描く。原本の回路図と同じ見た目になる。
#   電池は `battery1`（長い線＝正極）。原本と同じく**長い細線が正極・短い太線が負極**。
import os, subprocess, struct

TMPD = os.environ.get('TIKZ_TMP', '/tmp/tikzfig')
os.makedirs(TMPD, exist_ok=True)

HEAD = r"""\documentclass[border=3pt,dvipdfmx]{standalone}
\usepackage{amsmath}
\usepackage{tikz}
\usepackage[european,cute inductors,straightvoltages]{circuitikz}
\usetikzlibrary{arrows.meta,patterns,decorations.markings,calc}
\ctikzset{bipoles/length=1.1cm, resistors/scale=0.8, batteries/scale=0.9,
          capacitors/scale=0.8, inductors/scale=0.8, csources/scale=0.8}
\newcommand{\U}[1]{\,[\mathrm{#1}]}
\begin{document}
\begin{tikzpicture}[line join=round,line cap=round,
   ax/.style={line width=0.6pt,-{Latex[length=2.2mm,width=1.8mm]}},
   cur/.style={line width=0.7pt,-{Latex[length=2.0mm,width=1.6mm]}},
   frc/.style={-{Latex[length=2.4mm,width=2.0mm]},line width=1.0pt},
   dim/.style={line width=0.5pt,{Latex[length=1.6mm,width=1.4mm]}-{Latex[length=1.6mm,width=1.4mm]}},
   gd/.style={line width=0.4pt,dash pattern=on 1.2pt off 1.2pt},
   eq/.style={line width=0.5pt,dash pattern=on 1.6pt off 1.6pt},
   lab/.style={fill=white,inner sep=1pt}]
"""
TAIL = "\\end{tikzpicture}\n\\end{document}\n"


def remake_xbb(png):
    xbb = png[:-4] + '.xbb'
    if os.path.exists(xbb):
        os.remove(xbb)
    subprocess.run(['extractbb', png], capture_output=True)


def build(name, body, outdir='fig', head=HEAD):
    tex = os.path.join(TMPD, name + '.tex')
    open(tex, 'w', encoding='utf-8').write(head + body + TAIL)
    r = None
    for _ in range(2):
        r = subprocess.run(['uplatex', '-interaction=nonstopmode', '-halt-on-error',
                            '-output-directory', TMPD, tex],
                           capture_output=True, text=True)
    dvi = os.path.join(TMPD, name + '.dvi')
    if r.returncode != 0 or not os.path.exists(dvi):
        print('  !! コンパイル失敗', name)
        lines = r.stdout.splitlines()
        for i, l in enumerate(lines):
            if l.startswith('!'):
                print('\n'.join(lines[i:i+6]))
                break
        return None
    pdf = os.path.join(TMPD, name + '.pdf')
    subprocess.run(['dvipdfmx', '-q', '-o', pdf, dvi], capture_output=True)
    out = os.path.join(outdir, name + '.png')
    subprocess.run(['gs', '-q', '-sDEVICE=pnggray', '-r600', '-dNOPAUSE', '-dBATCH',
                    '-dTextAlphaBits=4', '-dGraphicsAlphaBits=4', '-o', out, pdf],
                   capture_output=True)
    remake_xbb(out)
    w, h = struct.unpack('>II', open(out, 'rb').read(64)[16:24])
    print('  %-24s %5dx%-5d (縦横比 %.3f)  %6.1f KB'
          % (os.path.basename(out), w, h, h / w, os.path.getsize(out) / 1000))
    return h / w


def run(figs, argv):
    """figs = {name: body}。argv に名前の一部が与えられればそれだけ作る。"""
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    only = [a for a in argv if not a.startswith('-')]
    for name, body in figs.items():
        if only and not any(k in name for k in only):
            continue
        build(name, body)

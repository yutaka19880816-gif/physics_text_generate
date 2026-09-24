#!/bin/bash
# 指定した章だけを組んで PDF にする（本体の 入試物理基礎演習.tex/.pdf には触れない）
#   使い方:  ./make_chapter.sh 1                    → 第1章のみ.pdf
#            ./make_chapter.sh 5                    → 第5章のみ.pdf
#            ./make_chapter.sh 15 --anaume         → 第15章のみ_穴埋め.pdf（生徒用）
#
# 紙面デザイン（butsuri_style.sty）は 2026-08-31 に本体プリアンブルへ組み込んだので
# --style は不要になった（付けても無視する）．
#
# --anaume を付けると \bsAnaumetrue が立ち，例題の解答の \Ana{式} が
# 「元の数式と同じ幅・高さの空欄」になる（生徒用の穴埋めプリント）．
# 寸法が完全版と一致するので，両者のページ送りは揃う．
#
# 本体の .tex には一切変更を加えない．どれも /tmp のラッパ経由で組む．
# ※ .tex を作業フォルダに残さない（VS Code が root と誤認するのを避けるため /tmp に作る）
set -e
N=${1:?章番号を指定してください（例: ./make_chapter.sh 1）}
ANAUME=0
for a in "$@"; do
  [ "$a" = "--anaume" ] && ANAUME=1
  [ "$a" = "--style" ]  && echo "（--style は不要です：紙面デザインは本体に組み込み済み）"
done

CH="physics_ch${N}"
JOB="第${N}章のみ"
[ "$ANAUME" = "1" ] && JOB="第${N}章のみ_穴埋め"
[ -f "${CH}.tex" ] || { echo "${CH}.tex がありません"; exit 1; }

python3 - "$CH" "$N" "$ANAUME" <<'PY'
import sys
ch, n_str = sys.argv[1], sys.argv[2]
anaume = sys.argv[3] == '1'
m=open('入試物理基礎演習.tex',encoding='utf-8').read()
i=m.index('\\begin{document}'); body=m[i:]
j=body.index('\\newpage\n\n{\\huge 入試物理基礎演習}')   # 表紙以降を捨て、マクロ定義だけ残す
# 前の章までの \Mon の個数を数えて qno を合わせる（章単体でも問題番号が本体と一致するように）
import re, os
n=int(n_str); qno=0
for k in range(1,n):
    f='physics_ch%d.tex'%k
    if os.path.exists(f):
        qno += len(re.findall(r'(?<!\\MonN)\\Mon(?:\[[^\]]*\])?\{', open(f,encoding='utf-8').read()))
pre   = m[:i]
macro = '\\begin{document}'+body[len('\\begin{document}'):j]
# 紙面デザインは本体プリアンブル側で読み込み・\ButsuriApply 済みなので，ここでは何もしない
apply_ = '\n\\bsAnaumetrue\n' if anaume else ''
# 節番号も本体と合わせる（physics_chN.tex ＝ 第N節）．これが無いと章単体では
# 見出しが必ず「1」になり，解答編の柱「第N回」と食い違う．
open('/tmp/_chap_only.tex','w',encoding='utf-8').write(
    pre+macro+apply_
    +'\n\\setcounter{section}{%d}\n'%(n-1)
    +'\n\\setcounter{qno}{%d}\n'%qno+'\n\\include{%s}\n'%ch+'\\end{document}\n')
PY

rm -f "${JOB}.aux" "${CH}.aux"
for i in 1 2; do platex -interaction=nonstopmode -jobname="$JOB" '\input{/tmp/_chap_only.tex}' >/dev/null 2>&1; done
echo -n "エラー        : "; grep -c '^!' "${JOB}.log" || true
echo -n "Overfull      : "; grep -c -i 'overfull' "${JOB}.log" || true
echo -n "Underfull     : "; grep -c -i 'underfull' "${JOB}.log" || true
# wrapfig は \usepackage の読み込み行も引っかかるので，警告だけを数える
echo -n "wrapfig警告   : "; grep -c -i 'wrapfig warning\|Collision between wrapping' "${JOB}.log" || true
grep "Output written" "${JOB}.log"
dvipdfmx "${JOB}.dvi" 2>&1 | grep -c 'unparsed' | xargs -I{} echo "未解釈special : {} 件（0なら図が正しく埋め込まれている）"
cp "${JOB}.log" "/tmp/${JOB}.log"    # 検証用にログだけ /tmp へ残す
rm -f "${JOB}.dvi" "${JOB}.aux" "${JOB}.log" "${JOB}.synctex.gz" /tmp/_chap_only.tex
ls -la "${JOB}.pdf" | awk '{printf "→ %s  %.2f MB\n",$9,$5/1000000}'

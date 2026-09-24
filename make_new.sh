#!/bin/bash
# 再編中の新しい回（physics_newN.tex）だけを組んで「第N回のみ.pdf」を作る。
#   使い方:  ./make_new.sh 14              → 第14回のみ.pdf
#            ./make_new.sh 14 --anaume     → 第14回のみ_穴埋め.pdf
# make_chapter.sh の physics_chN.tex 版に対する physics_newN.tex 版。
# 問題番号 qno と 例題番号 nombre は各 physics_newN.tex が自分で \setcounter する前提。
set -e
N=${1:?回番号を指定してください（例: ./make_new.sh 14）}
ANAUME=0
for a in "$@"; do [ "$a" = "--anaume" ] && ANAUME=1; done
CH="physics_new${N}"
JOB="第${N}回のみ"
[ "$ANAUME" = "1" ] && JOB="第${N}回のみ_穴埋め"
[ -f "${CH}.tex" ] || { echo "${CH}.tex がありません"; exit 1; }

python3 - "$CH" "$N" "$ANAUME" <<'PY'
import sys
ch, n_str, anaume = sys.argv[1], sys.argv[2], sys.argv[3]=='1'
m=open('入試物理基礎演習.tex',encoding='utf-8').read()
i=m.index('\\begin{document}'); body=m[i:]
j=body.index('\\newpage\n\n{\\huge 入試物理基礎演習}')
pre   = m[:i]
macro = '\\begin{document}'+body[len('\\begin{document}'):j]
apply_ = '\n\\bsAnaumetrue\n' if anaume else ''
open('/tmp/_new_only.tex','w',encoding='utf-8').write(
    pre+macro+apply_
    +'\n\\setcounter{section}{%d}\n'%(int(n_str)-1)
    +'\n\\include{%s}\n'%ch+'\\end{document}\n')
PY

rm -f "${JOB}.aux" "${CH}.aux"
# remember picture（\coldivider）を使う章のために2回通す
for i in 1 2; do platex -interaction=nonstopmode -jobname="$JOB" '\input{/tmp/_new_only.tex}' >/dev/null 2>&1; done
echo -n "エラー        : "; grep -c '^!' "${JOB}.log" || true
echo -n "Overfull      : "; grep -c -i 'overfull' "${JOB}.log" || true
echo -n "Underfull     : "; grep -c -i 'underfull' "${JOB}.log" || true
echo -n "wrapfig警告   : "; grep -c -i 'wrapfig warning\|Collision between wrapping' "${JOB}.log" || true
grep "Output written" "${JOB}.log"
dvipdfmx "${JOB}.dvi" 2>&1 | grep -c 'unparsed' | xargs -I{} echo "未解釈special : {} 件（0なら図が正しく埋め込まれている）"
cp "${JOB}.log" "/tmp/${JOB}.log"
rm -f "${JOB}.dvi" "${JOB}.aux" "${JOB}.synctex.gz" /tmp/_new_only.tex
ls -la "${JOB}.pdf" | awk '{printf "→ %s  %.2f MB\n",$9,$5/1000000}'

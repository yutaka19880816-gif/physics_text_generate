#!/bin/bash
# 指定した例題・練習問題から確認テストを作る（問題用紙＋解答解説用紙）
#
#   使い方:
#     ./make_test.sh 14 --rei 1,3 --ren 2,5 \
#         --title "第14回　確認テスト" --sub "気体の状態方程式・熱力学第一法則" \
#         --time 30 --score 25,25,25,25 --height 60,50,45,55
#
#     --rei    例題番号（カンマ区切り）
#     --ren    練習問題番号（カンマ区切り）
#     --title  問題用紙のタイトル（既定「第N回　確認テスト」）
#     --sub    副題（省略可）
#     --time   試験時間（分・省略可）
#     --score  各問の配点（カンマ区切り・省略可）．満点は自動合計
#     --height 各問の解答欄の高さ（mm・カンマ区切り）
#              省略すると解答欄を紙面の残りいっぱいまで広げる（実質1問1ページ）
#     --new    physics_chN.tex ではなく physics_newN.tex（再編後の回）から読む
#     --anszu  解答欄に作図用の枠を入れる（「概形を描け」の小問がある問題用）
#              書式: --anszu "問題番号:一辺mm[:形]:見出し"
#              形は maru（レンズの外周の円入り）／kaku（枠だけ・既定）／
#              画像のパス（作図の問題：問題の図をそのまま解答欄に置く）
#              例: --anszu "1:60:maru:(4) の図"
#                  --anszu "2:150:fig/n20_p64_zu.png:作図用"
#              複数の問題に付けるときは --anszu を繰り返す
#     --b4     B4横（JIS 364x257mm）1問1面にする．問題用紙は 左＝問題文／
#              右＝解答欄（ページの残り全部），解答解説用紙も同じ割り付けで
#              左＝問題文・指針／右＝解答．--height は無視される．
#
#   指定した順に第1問・第2問…と番号を振り直す（--rei が先，--ren が後）．
#
#   出力: 「第N回確認テスト_問題.pdf」「第N回確認テスト_解答.pdf」
#
# 問題文・指針・解答は physics_chN.tex から**読み取るだけ**で，教材側は
# 一切変更しない．本体プリアンブルをコピーしたラッパを /tmp に作って組むので，
# \U \Cel \Ans \ko komon zuright などの既存マクロがそのまま効く．
# ※ .tex を作業フォルダに残さない（VS Code が root と誤認するのを避ける）
set -e
N=${1:?章番号を指定してください（例: ./make_test.sh 14 --rei 1 --ren 2）}
shift
REI=""; REN=""; TITLE=""; SUB=""; TIME=""; SCORE=""; HEIGHT=""; NEW=0; B4=0; ANSZU=""
while [ $# -gt 0 ]; do
  case "$1" in
    --rei)    REI="$2";    shift 2;;
    --ren)    REN="$2";    shift 2;;
    --title)  TITLE="$2";  shift 2;;
    --sub)    SUB="$2";    shift 2;;
    --time)   TIME="$2";   shift 2;;
    --score)  SCORE="$2";  shift 2;;
    --height) HEIGHT="$2"; shift 2;;
    --anszu)  ANSZU="${ANSZU}${ANSZU:+|}$2"; shift 2;;
    --new)    NEW=1;       shift 1;;
    --b4)     B4=1;        shift 1;;
    *) echo "不明なオプション: $1"; exit 1;;
  esac
done
[ -z "$REI" ] && [ -z "$REN" ] && { echo "--rei か --ren のどちらかを指定してください"; exit 1; }

SRC="physics_ch${N}.tex"
[ "$NEW" = "1" ] && SRC="physics_new${N}.tex"
[ -f "$SRC" ] || { echo "$SRC がありません"; exit 1; }

python3 - "$N" "$SRC" "$REI" "$REN" "$TITLE" "$SUB" "$TIME" "$SCORE" "$HEIGHT" "$B4" "$ANSZU" <<'PY'
import sys, re, os
n, src, rei, ren, title, sub, time_, score, height, b4, anszu = sys.argv[1:12]
b4 = (b4 == '1')
# --anszu "1:60:(4)" → {1: ('60', '(4)')}
# --anszu "1:60:(4)" / "1:60:maru:(4)" / "2:150:fig/xx.png:作図用"
#   3つ目は maru（円入り）／kaku（枠だけ・既定）／画像のパス．無ければ見出し扱い
zu = {}
for e in [x for x in anszu.split('|') if x.strip()]:
    f = e.split(':', 3)
    k, size, rest = f[0], f[1], f[2:]
    shape = 'kaku'
    if rest and (rest[0] in ('maru', 'kaku') or '/' in rest[0] or '.' in rest[0]):
        shape, rest = rest[0], rest[1:]
    zu[int(k)] = (size, shape, rest[0] if rest else '')
s = open(src, encoding='utf-8').read()

# ---------------------------------------------------------------- 小道具
def read_group(t, i):
    """t[i] が '{' のとき，対応する '}' までの中身と，その次の位置を返す"""
    assert t[i] == '{', t[i:i+20]
    d = 0
    k = i
    while k < len(t):
        c = t[k]
        if c == '\\':          # \{ \} はエスケープなので飛ばす
            k += 2; continue
        if c == '{': d += 1
        elif c == '}':
            d -= 1
            if d == 0:
                return t[i+1:k], k+1
        k += 1
    raise ValueError('括弧が閉じていません')

def env_body(t, name, start=0):
    b, e = '\\begin{%s}' % name, '\\end{%s}' % name
    i = t.find(b, start)
    if i < 0: return None
    j = t.index(e, i)
    return t[i+len(b):j]

def strip_env(t, name):
    return re.sub(r'\\begin\{%s\}.*?\\end\{%s\}' % (name, name), '', t, flags=re.S)

# ---------------------------------------------------------------- 例題の抽出
# 例題番号は部（章）をまたいで通し．章ファイル冒頭の \setcounter{nombre}{N} が起点．
mb = re.search(r'\\setcounter\{nombre\}\{(\d+)\}', s)
nbase = int(mb.group(1)) if mb else 0
reidai = {}          # 番号 -> dict(theme, mondai, sisin, key, kaitou)
pos, k = 0, 0
while True:
    i = s.find('\\begin{reidaiunit}', pos)
    if i < 0: break
    j = s.index('\\end{reidaiunit}', i)
    unit = s[i:j]
    k += 1
    m = re.search(r'\\begin\{reidai\}', unit)
    theme, after = read_group(unit, m.end())
    mondai = unit[after:unit.index('\\end{reidai}', after)]
    mk = re.search(r'\\Key', unit)
    key = read_group(unit, mk.end())[0] if mk else ''
    reidai[nbase + k] = dict(theme=theme, mondai=mondai.strip(),
                     sisin=(env_body(unit, 'sisinE') or '').strip(),
                     key=key,
                     kaitou=(env_body(unit, 'kaitou') or '').strip())
    pos = j

# ---------------------------------------------------------------- 練習の抽出
# 問題編：\setcounter{qno}{N} 以降，解答編（\KaiTitle）より前
mq = re.search(r'\\setcounter\{qno\}\{(\d+)\}', s)
assert mq, '\\setcounter{qno}{...} が見つかりません'
qbase = int(mq.group(1))
q0 = mq.start()
q1 = s.index('\\KaiTitle')
qzone = s[q0:q1]
lines = qzone.split('\n')
renshu = {}
cur = None
# 見出し行は \Mon{テーマ} / \Mon[\Sitei]{テーマ}．テーマの後ろに \par\nopagebreak の
# ような指定が続く行もあるので，行末まで見る正規表現ではなく括弧を数えて読む．
MON_RE = re.compile(r'^\\Mon(?![A-Za-z])(\[[^\]]*\])?\{')
for ln in lines:
    m = MON_RE.match(ln)
    if m:
        theme = read_group(ln, m.end() - 1)[0]
        cur = dict(theme=theme, sitei=bool(m.group(1)), mondai=[])
        renshu[qbase + len(renshu) + 1] = cur
        continue
    if cur is not None:
        if ln.startswith(('\\Rank', '\\newpage')):
            cur = None; continue
        cur['mondai'].append(ln)
for v in renshu.values():
    v['mondai'] = '\n'.join(v['mondai']).strip()

# 解答編：multicols の中
a0 = s.index('\\begin{multicols}{2}')
a1 = s.index('\\end{multicols}', a0)
azone = s[a0:a1]
cur = None
# こちらも \MonN{48}{ヤングの実験}\par\nopagebreak のように後ろに続く行がある．
MONN_RE = re.compile(r'^\\MonN(\[[^\]]*\])?\{(\d+)\}\{')
for ln in azone.split('\n'):
    m = MONN_RE.match(ln)
    if m:
        cur = renshu[int(m.group(2))]
        cur['ans'] = []
        continue
    if cur is not None:
        if ln.startswith('\\Rank'):
            cur = None; continue
        cur['ans'].append(ln)
for v in renshu.values():
    body = '\n'.join(v.get('ans', [])).strip()
    body = strip_env(body, 'saikei')          # 要旨の再掲は使わない（全文を再掲する）
    v['sisin']  = (env_body(body, 'sisin') or '').strip()
    rest = re.sub(r'\\begin\{sisin\}.*?\\end\{sisin\}', '', body, count=1, flags=re.S)
    v['kaitou'] = rest.strip()                # kaitou と，あれば chuu をそのまま

# ---------------------------------------------------------------- 出題リスト
# 教材の紙面の都合で入っている改ページ指示は落とす．とくに \filbreak は
# multicols の中では段・ページを送ってしまい，解答解説が1面に収まらなくなる
# （第19回の練習58の問題文末尾にあり，裏面が問題文だけになった）．
LAYOUT = re.compile(r'\\(?:filbreak|newpage|clearpage|pagebreak|nopagebreak|'
                    r'enlargethispage)\*?(?:\[[^\]]*\])?|\\bsNeed\{[^}]*\}')
def strip_layout(t): return LAYOUT.sub('', t)

def nums(x): return [int(v) for v in x.split(',') if v.strip()]
items = []
for r in nums(rei):
    assert r in reidai, '例題%d が見つかりません' % r
    d = reidai[r]
    items.append(dict(src='例題%d' % r, theme=d['theme'], mondai=d['mondai'],
                      sisin=d['sisin'], key=d['key'], kaitou=d['kaitou']))
for r in nums(ren):
    assert r in renshu, '練習%d が見つかりません' % r
    d = renshu[r]
    items.append(dict(src='練習%d' % r, theme=d['theme'], mondai=d['mondai'],
                      sisin=d['sisin'], key='', kaitou=d['kaitou']))
for it in items:
    for k in ('mondai', 'sisin', 'kaitou'):
        it[k] = strip_layout(it[k]).strip()

sc = nums(score) if score else []
hs = nums(height) if height else []
assert not sc or len(sc) == len(items), '--score の個数が問題数と合いません'
assert not hs or len(hs) == len(items), '--height の個数が問題数と合いません'
total = str(sum(sc)) if sc else ''
title = title or ('第%s回　確認テスト' % n)

# ---------------------------------------------------------------- ラッパ生成
m = open('入試物理基礎演習.tex', encoding='utf-8').read()
i = m.index('\\begin{document}'); body = m[i:]
j = body.index('\\newpage\n\n{\\huge 入試物理基礎演習}')   # 表紙以降を捨て，マクロ定義だけ残す
# butsuri_style は本体プリアンブルが読み込み済み（2026-08-31）．ここでは butsuri_test だけ足す
pre = m[:i].replace('\\usepackage{butsuri_style}',
                    '\\usepackage{butsuri_style}\n\\usepackage{butsuri_test}', 1)
assert '\\usepackage{butsuri_test}' in pre, 'butsuri_test の挿入に失敗'
# B4横（JIS 364x257mm）．jsarticle は \mag を使うので寸法は必ず truemm で書く．
B4PRE = r'''
%% ---- B4横（JIS 364x257mm）確認テスト用の版面 ----
\setlength{\paperwidth}{364truemm}
\setlength{\paperheight}{257truemm}
\setlength{\textwidth}{340truemm}
\setlength{\textheight}{233truemm}
\setlength{\oddsidemargin}{12truemm}\addtolength{\oddsidemargin}{-1truein}
\setlength{\evensidemargin}{\oddsidemargin}
\setlength{\topmargin}{12truemm}\addtolength{\topmargin}{-1truein}
\addtolength{\topmargin}{-\headheight}\addtolength{\topmargin}{-\headsep}
\setlength{\footskip}{10truemm}
\AtBeginDvi{\special{papersize=364truemm,257truemm}}
'''
# \ButsuriApply も本体のマクロ定義の直後で呼ばれているので，ここでは足さない
macro = '\\begin{document}' + body[len('\\begin{document}'):j]

def esc(x):   # \TestHeader などの引数に素通しする
    return x

# --- 問題用紙 -------------------------------------------------------
if b4:
    # B4横・1問1面（左＝問題文，右＝解答欄）
    out = [macro,
           '\\pagestyle{empty}\n',
           '\\TestHeaderWide{%s}{%s}{%s}{%s}\n' % (title, sub, time_, total)]
    for k, it in enumerate(items, 1):
        if k > 1:
            out.append('\\newpage\n\\TestHeaderMini{%s}{%s}\n'
                       % (title, '（裏面）' if k == 2 else ''))
        opt = ''
        if k in zu:
            size, shape, cap = zu[k]
            if shape in ('maru', 'kaku'):
                opt = '[\\Sakuzu%s{%s}{%s}]' % ('Maru' if shape == 'maru' else 'Box',
                                                 size, cap)
            else:   # 画像のパス：問題の図をそのまま解答欄に置く
                opt = '[\\SakuzuZu{%s}{%s}{%s}]' % (size, shape, cap)
        out.append('\\begin{toipage}%s{%d}{%s}{%s}\n'
                   % (opt, k, it['theme'], sc[k-1] if sc else ''))
        out.append(it['mondai'] + '\n')
        out.append('\\end{toipage}\n')
else:
    out = [macro,
           '\\pagestyle{plain}\n',
           '\\TestHeader{%s}{%s}{%s}{%s}\n' % (title, sub, time_, total)]
    for k, it in enumerate(items, 1):
        out.append('\\ToiHead{%d}{%s}{%s}\n' % (k, it['theme'], sc[k-1] if sc else ''))
        out.append(it['mondai'] + '\n')
        # --height を書かなければ紙面の残りいっぱいまで広げる
        out.append('\\AnswerBox{%dmm}\n' % hs[k-1] if hs else '\\AnswerBoxFill\n')
out.append('\\end{document}\n')
open('/tmp/_test_q.tex', 'w', encoding='utf-8').write(
    (pre + B4PRE if b4 else pre) + ''.join(out))

# --- 解答解説用紙 ---------------------------------------------------
def kaitou_tex(it):
    # 練習は kaitou 環境ごと，または \KaiHead（解答の帯）で始まる形で入っている．
    # どちらも「解答」の帯を自分で出すので，重ねて kaitou で囲まない．
    # 先頭のコメント行・空行は読み飛ばして判定する（\MonN の直後に注記の
    # コメントが入っている章がある：これを見落として帯が2本出た）
    head = ''
    for ln in it['kaitou'].split('\n'):
        if ln.strip() and not ln.lstrip().startswith('%'):
            head = ln.lstrip(); break
    if head.startswith('\\begin{kaitou}') or head.startswith('\\KaiHead'):
        return it['kaitou'] + '\n'
    return '\\begin{kaitou}\n' + it['kaitou'] + '\n\\end{kaitou}\n'

def shrink_fig(t, r=0.70):
    # 解答解説の「問題の再掲」では図を r 倍に縮める（1面に収めるため）．
    # zuright の段幅と \includegraphics の width を同じ比で揃えて縮める．
    f = lambda m: '%s%.1fmm' % (m.group(1), float(m.group(2)) * r)
    t = re.sub(r'(\\begin\{zuright\}\{)(\d+(?:\.\d+)?)mm', f, t)
    return re.sub(r'(width=)(\d+(?:\.\d+)?)mm', f, t)

soltitle = '%s　解答・解説' % title
if b4:
    # B4横・1問1面（左＝問題文と指針，右＝解答）
    out = [macro, '\\pagestyle{empty}\n', '\\bsSolTight{0}\n',
           '\\SolTitle{%s}\n' % soltitle]
    for k, it in enumerate(items, 1):
        tag = it['src'] + ('／%d点' % sc[k-1] if sc else '')
        if k > 1:
            out.append('\\newpage\n\\TestHeaderMini{%s}{%s}\n'
                       % (soltitle, '（裏面）' if k == 2 else ''))
        out.append('\\begin{toipagesol}{%d}{%s}{%s}\n' % (k, it['theme'], tag))
        # mondaibun（framed）は multicols の中に置けないので帯だけの版を使う
        out.append('\\begin{mondaibunC}\n' + shrink_fig(it['mondai']) + '\n\\end{mondaibunC}\n')
        if it['sisin']:
            out.append('\\begin{sisinE}\n' + it['sisin'] + '\n\\end{sisinE}\n')
        if it['key']:
            out.append('\\Key{%s}\n' % it['key'])
        out.append(kaitou_tex(it))
        out.append('\\end{toipagesol}\n')
else:
    out = [macro, '\\pagestyle{plain}\n', '\\SolTitle{%s}\n' % soltitle]
    for k, it in enumerate(items, 1):
        tag = it['src'] + ('／%d点' % sc[k-1] if sc else '')
        out.append('\\SolHead{%d}{%s}{%s}\n' % (k, it['theme'], tag))
        out.append('\\begin{mondaibun}\n' + it['mondai'] + '\n\\end{mondaibun}\n')
        if it['sisin']:
            out.append('\\begin{sisinE}\n' + it['sisin'] + '\n\\end{sisinE}\n')
        if it['key']:
            out.append('\\Key{%s}\n' % it['key'])
        out.append(kaitou_tex(it))
out.append('\\end{document}\n')
open('/tmp/_test_a.tex', 'w', encoding='utf-8').write(
    (pre + B4PRE if b4 else pre) + ''.join(out))

print('出題: ' + '，'.join('第%d問=%s（%s）' % (k, it['src'], it['theme'])
                          for k, it in enumerate(items, 1)))
PY

build () {   # $1=ラッパ  $2=ジョブ名
  rm -f "$2.aux"
  for i in 1 2; do platex -interaction=nonstopmode -jobname="$2" "\\input{$1}" >/dev/null 2>&1; done
  echo -n "  エラー        : "; grep -c '^!' "$2.log" || true
  echo -n "  Overfull      : "; grep -c -i 'overfull' "$2.log" || true
  echo -n "  Underfull     : "; grep -c -i 'underfull' "$2.log" || true
  echo -n "  wrapfig警告   : "; grep -c -i 'wrapfig warning\|Collision between wrapping' "$2.log" || true
  grep "Output written" "$2.log" | sed 's/^/  /'
  dvipdfmx "$2.dvi" 2>&1 | grep -ci 'unparsed' | xargs -I{} echo "  未解釈special : {} 件（0なら図が正しく埋め込まれている）"
  cp "$2.log" "/tmp/$2.log"
  rm -f "$2.dvi" "$2.aux" "$2.log" "$2.synctex.gz"
}

pages () { sed -n 's/.*Output written on .*(\([0-9]*\) pages.*/\1/p' "/tmp/$1.log"; }

echo "── 問題用紙 ──"; build /tmp/_test_q.tex "第${N}回確認テスト_問題"
echo "── 解答解説 ──"; build /tmp/_test_a.tex "第${N}回確認テスト_解答"
# --b4 は「1問1面」．解答があふれて面数が増えたら，字送りを1段階ずつ詰めて
# 組み直す（\bsSolTight 0→1→2）．それでも収まらないときは諦めてそのまま出す．
if [ "$B4" = "1" ]; then
  NITEMS=$(echo "${REI},${REN}" | tr ',' '\n' | grep -c '[0-9]')
  for LVL in 1 2; do
    P=$(pages "第${N}回確認テスト_解答")
    [ -z "$P" ] && break
    [ "$P" -le "$NITEMS" ] && break
    echo "  （解答が ${P} 面になったので \\bsSolTight{${LVL}} で組み直します）"
    sed -i '' "s/\\\\bsSolTight{[0-9]}/\\\\bsSolTight{${LVL}}/" /tmp/_test_a.tex
    build /tmp/_test_a.tex "第${N}回確認テスト_解答"
  done
fi
rm -f /tmp/_test_q.tex /tmp/_test_a.tex
ls -la "第${N}回確認テスト_問題.pdf" "第${N}回確認テスト_解答.pdf" | awk '{printf "→ %s  %.2f MB\n",$9,$5/1000000}'

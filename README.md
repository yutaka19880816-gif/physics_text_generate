# 入試物理基礎演習

鉄緑会「入試物理基礎演習」を upLaTeX で組み直したもの。
**46回構成 → 34回構成への再編**が進行中で、旧構成（`physics_chN.tex`）と
新構成（`physics_newN.tex`）が並走している。

## 新しい回を作るときの入口

1. **`組版チェックリスト.md`** を先に開く（工程順の手順書。ここに書いてある地雷は全部踏んだもの）
2. `saihen/再編案.md` … 新しい回の構成と進捗
3. `saihen/daicho.md` … 練習239題の台帳（番号・ランク・テーマ・設定）
4. `./make_new.sh N` … 「第N回のみ.pdf」を作る（`--anaume` で生徒用の穴埋め版）

## フォルダ構成

| | 中身 |
|---|---|
| `入試物理基礎演習.tex` | 本体のマスター。`physics_ch1〜46` を `\include` する |
| `physics_ch1〜46.tex` | **旧46回構成**。第1〜13回（力学）は配布済みで据え置き、ch19〜24・ch26〜46 は**これから作る第19〜34回の素材**なので現役 |
| `physics_new14〜24.tex` | **再編後の回**（完成済み：第14〜20回＝第2章 波動／第21〜23回＝第3章 熱力学／第24回＝第4章 電磁気学の初回） |
| `butsuri_style.sty` | 紙面デザイン（黒ベタの番号バッジ・4種の罫・穴埋め版マクロなど） |
| `img/scan/` | 問題編のページスキャン（`prob_p*` 第1巻／`prob2_p*` 第2巻）＋ `.xbb` |
| `img/text/` | 講義編から切った図（`text_p*` 第1巻／`text2_p*` 第2巻）＋ `.xbb` |
| `fig/` | TeX化のときに切り出した図（`n17_*`, `ch25_*` など）。`fig/orig_halftone/` は網点図の原本退避 |
| `texify_draft/` | 切り出し・検査スクリプトと下書き |
| `saihen/` | 再編の設計文書と問題台帳 |
| `archive/` | 過去の遺物（下記）。**参照しているものは何も無い** |

### スクリプト

| | |
|---|---|
| `make_new.sh N` | 第N回のみを組む（再編後の `physics_newN.tex`） |
| `make_chapter.sh N` | 第N章のみを組む（旧構成の `physics_chN.tex`） |
| `make_test.sh` | 確認テスト（問題用紙＋解答解説）を作る |
| `texify_draft/wfcheck.py` | **組む前**：wrapfigure の `[N]` 不足／`\bsNeed` の欠落を指摘 |
| `texify_draft/pagecheck.py` | **組んだ後**：紙面はみ出し／本文幅／余白の紙面比 |
| `texify_draft/figprobe.py` | 切り出し窓を決めるための行・列インク量の実測 |
| `texify_draft/blocks.py` | 列ストリップを空白帯でブロック分割し，図の候補（密度の低いブロック）を探す |
| `texify_draft/pnggrid.py` | ページに座標グリッドを重ねた縮小PNGを作る（窓を目で読む用） |
| `texify_draft/pngslope.py` | 原本スキャンの傾きを測る（見開きでもページごとに違う） |
| `texify_draft/mkfig_newN.py` ＋ `jobs_newN.py` | 第N回の図を全部作る（切り出し座標は jobs 側。`--halftone` で網点処理だけやり直す） |
| `texify_draft/mkfig_newNans.py` | 第N回の解答の図を TikZ で自作する（`_blank` は `\AnaFig` の補助図） |

## 画像のパスについて（2026-09-05 に整理）

画像はルート直下に平置きされていたが、`img/scan/`・`img/text/` に集約した。
**参照の書き方は変えなくてよい。**

- `.tex` の `\includegraphics{text_p106_fig1.png}` … `入試物理基礎演習.tex` の
  `\graphicspath{{./}{img/text/}{img/scan/}{fig/}}` が解決する（`.xbb` の探索にも効く）
- `jobs_new*.py` の `('prob_p58.png', 'fig/n17_p30_mic.png', ...)` … `texify_draft/imgpath.py` が解決する

**出力側は今までどおり `fig/` を明示して書くこと**（`imgpath` は読み込みしか通していない）。
`extractbb` は画像のある場所でかける（`extractbb img/text/foo.png`）。

## archive/ の中身

| | |
|---|---|
| `bak/` | `*.bak_*` … 編集前のバックアップ76件 |
| `旧マスター/` | `入試物理の基礎演習.tex/.pdf`（2020年版の前身）と `physics_main.*`（`.tex` はもう存在しない死んだジョブの生成物） |
| `旧章単位の出力/` | 「第N章のみ*.pdf」… 旧構成の章単位の出力。`第25章のみ.pdf` は余白比較の基準（17%） |
| `build/` | `*.aux` `*.log` `*.toc` `*.dvi` `*.synctex.gz` … 組み直せば再生成される |
| `その他/` | 無関係な数学ファイル、`eclbkbox.zip` |

ビルドすると `*.aux` / `*.log` などがまたルート直下に出る（本体を組むと `physics_chN.aux` が46個）。
捨ててよいものなので、気になったら `archive/build/` へ掃き出せばよい。ただし `入試物理基礎演習.aux` と
`.toc` を消すと相互参照の解決に3パス必要になる（もともと3回まわす決まりなので実害はない）。

# -*- coding: utf-8 -*-
"""画像を「ファイル名だけ」で書けるようにするパス解決。

2026-09-05 に画像をルート直下から下記へ移した：
    img/scan/ … 問題編のページスキャン（prob_p*, prob2_p*）
    img/text/ … 講義編から切った図（text_p*, text2_p*）
    fig/      … TeX化のときに切り出した図

これに合わせて jobs_new*.py / mkfig_ch*.py の 200 箇所を書き換えるのは事故のもとなので、
**読み込み側（pngcrop_local.load_gray / pnglighten.decode / pngtrim.decode）だけ**が
この resolve() を通す。おかげでジョブ定義は今までどおり

    ('prob_p58.png', 'fig/n17_p30_mic.png', 2700, 2560, 540, 1010)

と素のファイル名で書ける。新しい切り出しを書くときも同じでよい。

書き出し側（save_gray / write_gray）は通していない。出力は 'fig/n17_*.png' のように
明示パスで書く決まりなので、うっかり img/ の下に吐くのを防ぐため。
"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SEARCH = ['', 'img/scan', 'img/text', 'fig']


def resolve(path):
    """path が見つからなければ img/scan・img/text・fig の順に探して実在するパスを返す。
       どこにも無ければ path をそのまま返す（呼び出し元で従来どおり FileNotFoundError にする）。"""
    if os.path.exists(path):
        return path
    for d in SEARCH:
        p = os.path.join(ROOT, d, path)
        if os.path.exists(p):
            return p
    return path

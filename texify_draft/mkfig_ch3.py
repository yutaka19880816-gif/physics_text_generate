# -*- coding: utf-8 -*-
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pngtrim import ink_bbox

SOURCE = '/Users/yutaka/Documents/入試物理基礎演習'
OUT = os.path.join(SOURCE, 'fig')
TMP = '/tmp/_mkfig_ch3_rough.png'
os.makedirs(OUT, exist_ok=True)


def sips(args):
    subprocess.run(['sips'] + args, check=True, capture_output=True)


def pixel_width(path):
    result = subprocess.run(
        ['sips', '--getProperty', 'pixelWidth', path], check=True,
        capture_output=True, text=True
    )
    match = re.search(r'pixelWidth:\s*(\d+)', result.stdout)
    if match is None:
        raise RuntimeError(f'pixelWidthを取得できません: {path}')
    return int(match.group(1))


def make(src_name, out_name, left, top, width, height, placed_mm, margin=20):
    """粗窓を検査してから自動トリムし、必要なら360dpiへ縮小する。"""
    src = os.path.join(SOURCE, src_name)
    out = os.path.join(OUT, out_name)
    sips(['-c', str(height), str(width), '--cropOffset', str(top), str(left),
          src, '--out', TMP])
    box = ink_bbox(TMP)
    if box is None:
        raise RuntimeError(f'{out_name}: 粗窓内にインクがありません')
    x0, y0, x1, y1, crop_w, crop_h = box

    # 粗窓の時点でインクが四辺のどこかに触れていたら、自動トリムでは
    # 欠けを救えないので、その図を生成せず停止する。
    if not (x0 > 0 and y0 > 0 and x1 < crop_w - 1 and y1 < crop_h - 1):
        raise RuntimeError(
            f'{out_name}: 粗窓が狭すぎます '
            f'(bbox={x0},{y0},{x1},{y1}; window={crop_w}x{crop_h})'
        )

    final_left = max(1, left + x0 - margin)
    final_top = max(1, top + y0 - margin)
    final_w = x1 - x0 + 1 + 2 * margin
    final_h = y1 - y0 + 1 + 2 * margin
    sips(['-c', str(final_h), str(final_w), '--cropOffset', str(final_top),
          str(final_left), src, '--out', out])

    target_px = round(placed_mm / 25.4 * 360)
    if final_w > target_px:
        sips(['--resampleWidth', str(target_px), out])
        final_w = target_px

    print(f'{out_name:20s} {final_w:4d}px  {placed_mm:g}mm  <=360dpi')


# (source, output, left, top, rough width, rough height, placed width in mm)
jobs = [
    # 解答の作用図13枚
    ('prob_p72_2.png', 'ch3_p72_19a.png', 3280, 1080, 290, 500, 20),
    ('prob_p72_2.png', 'ch3_p72_19b.png', 3150, 1560, 400, 570, 24),
    ('prob_p72_2.png', 'ch3_p72_19c.png', 3150, 2130, 420, 430, 28),
    ('prob_p73.png', 'ch3_p73_20.png', 80, 1, 1750, 1050, 70),
    ('prob_p73.png', 'ch3_p73_21.png', 450, 3700, 950, 700, 50),
    ('prob_p73.png', 'ch3_p73_22.png', 2400, 2050, 950, 900, 60),
    ('prob_p74.png', 'ch3_p74_23a.png', 500, 880, 780, 570, 55),
    ('prob_p74.png', 'ch3_p74_23b.png', 500, 3110, 780, 450, 55),
    ('prob_p74.png', 'ch3_p74_24.png', 2380, 1220, 800, 650, 60),
    ('prob_p75.png', 'ch3_p75_25.png', 550, 170, 730, 620, 50),
    ('prob_p75.png', 'ch3_p75_26.png', 400, 4060, 1000, 780, 62),
    ('prob_p75.png', 'ch3_p75_27a.png', 2460, 3720, 760, 480, 55),
    ('prob_p76_1.png', 'ch3_p76_27b.png', 400, 50, 760, 500, 55),

    # 既存問題図3枚の切り直し
    ('prob_p10.png', 'ch3_p10_26.png', 2600, 200, 1050, 1800, 42),
    ('prob_p9.png', 'ch3_p9_24.png', 2620, 1250, 950, 1480, 30),
    ('prob_p8.png', 'ch3_p8_19c.png', 2600, 650, 1050, 950, 45),
]


for job in jobs:
    make(*job)


# 既存の網点図も、実際の貼付幅で360dpiを超える場合は縮小する。
existing_resamples = [
    ('ch3_p8_19a.png', 20),
    ('ch3_p8_20.png', 36.5),
    ('ch3_p9_23.png', 48),
]
for name, placed_mm in existing_resamples:
    path = os.path.join(OUT, name)
    target_px = round(placed_mm / 25.4 * 360)
    if pixel_width(path) > target_px:
        sips(['--resampleWidth', str(target_px), path])
    print(f'{name:20s} {pixel_width(path):4d}px  {placed_mm:g}mm  <=360dpi')


# dvipdfmxがPNGを確実に読めるよう、生成・更新した全画像にxbbを付ける。
for name in [job[1] for job in jobs] + [job[0] for job in existing_resamples]:
    subprocess.run(['extractbb', name], cwd=OUT, check=True)

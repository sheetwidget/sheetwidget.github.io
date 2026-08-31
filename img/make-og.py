#!/usr/bin/env python3
"""OG画像(1200x630)を全言語ぶん生成する。

デザインは既存版から実測して再現している：
  背景 #FBFAF6 / 48px方眼 #ECEAE2 / 上部に8pxの緑帯 / 中央にアプリアイコン
  太字の見出し2行 / 下部に緑のブランド名
文言を変えたい時は HEADLINES を直すだけでよい。実行は `python3 img/make-og.py`。
"""
import sys

from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 630
BG = (251, 250, 246)
GRID = (236, 234, 226)
GREEN = (24, 128, 56)
INK = (27, 29, 31)
CELL = 48
BAR_H = 8
BRAND = "Sheet Widget"

# 2行の見出し。長すぎると自動で縮むが、意味の切れ目で手で割った方がきれい。
HEADLINES = {
    "ja": ["スプレッドシートを、", "ホーム画面に。"],
    "en": ["Your Google Sheets,", "on your Home Screen."],
    "de": ["Deine Google-Tabellen,", "auf dem Home-Bildschirm."],
    "es": ["Tus hojas de Google,", "en la pantalla de inicio."],
    "fr": ["Vos feuilles Google,", "sur votre écran d’accueil."],
    "ko": ["구글 스프레드시트를,", "홈 화면에."],
    "zht": ["把 Google 試算表,", "放到主畫面。"],
}
# 出力名だけ既存に合わせる（ja は og.png も兼ねる）
EXTRA_COPIES = {"ja": ["og.png"]}

LATIN = "/System/Library/Fonts/HelveticaNeue.ttc"
# 日本語は「ヒラギノ角ゴシック(Hiragino Sans)」。名前の似た "Hiragino Sans GB"
# は簡体字中国語版で、一部の漢字が中国語の字形になり日本語として不自然になる。
JA = "/System/Library/Fonts/ヒラギノ角ゴシック W7.ttc"
CJK = "/System/Library/Fonts/Hiragino Sans GB.ttc"


def font_for(lang, size):
    """日本語はヒラギノ角ゴシック、韓中は Hiragino Sans GB、他は Helvetica Neue Bold。"""
    if lang == "ja":
        return ImageFont.truetype(JA, size, index=0)    # Hiragino Sans W7
    if lang in ("ko", "zht"):
        return ImageFont.truetype(CJK, size, index=2)   # W6 = 太字
    return ImageFont.truetype(LATIN, size, index=1)     # Bold


def draw_grid(d):
    for x in range(0, W, CELL):
        d.line([(x, BAR_H), (x, H)], fill=GRID, width=1)
    for y in range(BAR_H, H, CELL):
        d.line([(0, y), (W, y)], fill=GRID, width=1)


def fit(d, lines, lang, start=76, margin=64):
    """2行とも収まる最大の字号を返す。"""
    size = start
    while size > 28:
        f = font_for(lang, size)
        if all(d.textlength(t, font=f) <= W - margin * 2 for t in lines):
            return f
        size -= 2
    return font_for(lang, 28)


def build(lang, lines, icon):
    im = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(im)
    draw_grid(d)
    d.rectangle([0, 0, W, BAR_H - 1], fill=GREEN)

    # icon.png は角丸のない正方形なので、iOS 相当(辺の22.37%)の角丸で抜く
    ic = icon.resize((144, 144), Image.LANCZOS)
    mask = Image.new("L", (144 * 4, 144 * 4), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, 144 * 4 - 1, 144 * 4 - 1],
                                           radius=int(144 * 4 * 0.2237), fill=255)
    ic.putalpha(mask.resize((144, 144), Image.LANCZOS))
    im.paste(ic, (W // 2 - 72, 48), ic)

    f = fit(d, lines, lang)
    asc, desc = f.getmetrics()
    lh = int((asc + desc) * 1.18)
    top = 250 - lh // 2
    for i, t in enumerate(lines):
        d.text((W // 2, top + i * lh), t, font=f, fill=INK, anchor="ma")

    fb = font_for(lang, 34) if lang not in ("ja", "ko", "zht") else font_for("en", 34)
    d.text((W // 2, 545), BRAND, font=fb, fill=GREEN, anchor="ma")
    return im


# ── 言語に依存しないカード ──────────────────────────────────
# SNSのクローラは閲覧者の言語を見ないため、言語別の見出しを載せると
# どの言語で共有しても英語版か日本語版のどちらかに固定されてしまう。
# そこで共有用の1枚は文字を商品名だけにし、表計算らしさは
# 行番号と列見出し（数字とアルファベット＝どの言語でも読める）で出す。

HEAD_BAND = (243, 241, 235)   # 列見出し・行番号の帯
HEAD_LINE = (223, 220, 210)   # 帯の境界
HEAD_INK  = (150, 146, 136)   # 帯の文字
SELECT    = (242, 160, 42)    # 選択範囲の枠。アプリアイコンの橙と揃える


def draw_sheet_chrome(d):
    """表計算の外枠。上に列見出し(A,B,C…)、左に行番号(1,2,3…)を敷く。"""
    band = 40                      # 帯の太さ
    top = BAR_H
    d.rectangle([0, top, W, top + band], fill=HEAD_BAND)
    d.rectangle([0, top, band, H], fill=HEAD_BAND)
    f = ImageFont.truetype(LATIN, 19, index=0)

    x = band
    for i in range(30):
        if x >= W:
            break
        d.text((x + CELL / 2, top + band / 2), chr(65 + i), font=f, fill=HEAD_INK, anchor="mm")
        x += CELL
    y = top + band
    for i in range(30):
        if y >= H:
            break
        d.text((band / 2, y + CELL / 2), str(i + 1), font=f, fill=HEAD_INK, anchor="mm")
        y += CELL
    d.line([(band, top), (band, H)], fill=HEAD_LINE, width=1)
    d.line([(0, top + band), (W, top + band)], fill=HEAD_LINE, width=1)


def build_neutral(icon):
    im = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(im)
    draw_grid(d)
    draw_sheet_chrome(d)
    d.rectangle([0, 0, W, BAR_H - 1], fill=GREEN)

    # 中央の「選択されたセル範囲」。ここだけ白く抜いて、その中に商品名を置く。
    box = [W // 2 - 300, 196, W // 2 + 300, 470]
    d.rounded_rectangle(box, radius=10, fill=(255, 255, 255), outline=SELECT, width=4)
    # 選択ハンドル（右下の小さな四角）。スプレッドシートの見慣れた記号
    d.rectangle([box[2] - 7, box[3] - 7, box[2] + 7, box[3] + 7], fill=SELECT,
                outline=(255, 255, 255), width=2)

    ic = icon.resize((132, 132), Image.LANCZOS)
    mask = Image.new("L", (132 * 4, 132 * 4), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, 132 * 4 - 1, 132 * 4 - 1],
                                           radius=int(132 * 4 * 0.2237), fill=255)
    ic.putalpha(mask.resize((132, 132), Image.LANCZOS))
    im.paste(ic, (W // 2 - 66, 228), ic)

    # 枠の上下に同じだけ余白が残る位置。文字が下線に触れると窮屈に見える。
    f = ImageFont.truetype(LATIN, 60, index=1)
    d.text((W // 2, 374), BRAND, font=f, fill=INK, anchor="ma")
    return im


def main():
    icon = Image.open("img/icon.png").convert("RGBA")
    # 既定は共有用の1枚だけ。言語別が要るときは --per-language を付ける。
    if "--per-language" in sys.argv:
        for lang, lines in HEADLINES.items():
            im = build(lang, lines, icon)
            for name in [f"og-{lang}.png"] + EXTRA_COPIES.get(lang, []):
                im.save(f"img/{name}")
                print("wrote img/" + name)
        return
    build_neutral(icon).save("img/og.png")
    print("wrote img/og.png")


if __name__ == "__main__":
    main()

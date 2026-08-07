#!/usr/bin/env python3
"""OG画像(1200x630)を全言語ぶん生成する。

デザインは既存版から実測して再現している：
  背景 #FBFAF6 / 48px方眼 #ECEAE2 / 上部に8pxの緑帯 / 中央にアプリアイコン
  太字の見出し2行 / 下部に緑のブランド名
文言を変えたい時は HEADLINES を直すだけでよい。実行は `python3 img/make-og.py`。
"""
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


def main():
    icon = Image.open("img/icon.png").convert("RGBA")
    for lang, lines in HEADLINES.items():
        im = build(lang, lines, icon)
        for name in [f"og-{lang}.png"] + EXTRA_COPIES.get(lang, []):
            im.save(f"img/{name}")
            print("wrote img/" + name)


if __name__ == "__main__":
    main()

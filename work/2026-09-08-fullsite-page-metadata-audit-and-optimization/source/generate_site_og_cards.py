# -*- coding: utf-8 -*-
"""
生成全站主要頁面符合 Facebook / Twitter 標準的 1200x630 高解析度 OG 社群分享大卡片
"""
import os
import sys
from PIL import Image, ImageDraw, ImageFont

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = r"d:\@Codex\594katchang-source.github.io-main"
ASSETS_OG_DIR = os.path.join(BASE_DIR, "assets", "og")
OUTPUT_DIR = os.path.join(BASE_DIR, "work", "2026-09-08-fullsite-page-metadata-audit-and-optimization", "output", "og_images")

os.makedirs(ASSETS_OG_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

FONT_BOLD = r"C:\Windows\Fonts\msjhbd.ttc"
FONT_REGULAR = r"C:\Windows\Fonts\msjh.ttc"
AVATAR_PATH = os.path.join(BASE_DIR, "assets", "profile", "kat-avatar.jpg")

PAGES_CONFIG = [
    {
        "filename": "og-home.png",
        "badge": "整合健康教育與實證轉譯 ｜ Kat Chang 營養生活誌",
        "badge_color": (33, 100, 110),
        "title": "Kat Chang 營養師的健康生活誌",
        "subtitle": "實證營養 × 身心減壓 × 樂齡培訓 ｜ 專業講師、諮詢與互動教具",
        "highlights": ["三大支柱：長者營養、職場減壓、身心自癒", "全系列原創互動數位教具開放免費體驗", "收錄逾萬字國際期刊文獻轉譯衛教專欄"],
        "bg_gradient": ((18, 34, 48), (28, 62, 75)),
        "accent_color": (80, 227, 194),
        "accent_badge_text": "官方首頁",
        "author_desc": "台北醫學大學 ｜ 國家高考營養師"
    },
    {
        "filename": "og-about.png",
        "badge": "專業資歷與核心理念 ｜ 營養師 Kat Chang",
        "badge_color": (30, 80, 120),
        "title": "關於 Kat Chang 營養師",
        "subtitle": "台北醫學大學保健營養學系 ｜ 國家高考營養師、樂齡運動指導員",
        "highlights": ["百場企業內訓與社區樂齡衛教演講經驗", "擅長以有溫度的科學語言轉譯醫學新知", "專注高齡衰弱預防、職場壓力調節與情緒飲食"],
        "bg_gradient": ((20, 36, 52), (32, 64, 88)),
        "accent_color": (129, 212, 250),
        "accent_badge_text": "專業資歷",
        "author_desc": "資深衛教講師 ｜ 身心靈植癒引導"
    },
    {
        "filename": "og-class.png",
        "badge": "專業演講、企業內訓與社區培訓 ｜ 邀約合作",
        "badge_color": (120, 60, 40),
        "title": "課程講座與授課經歷 ｜ Kat Chang",
        "subtitle": "樂齡健康促進、企業舒壓防疲勞、互動式營養工作坊",
        "highlights": ["社區關懷據點與長青學苑長者實體生動教學", "科技業、金融業高階白領抗疲勞身心工作坊", "結合 NutriRank 與線上教具的沉浸式互動演練"],
        "bg_gradient": ((45, 25, 30), (75, 40, 45)),
        "accent_color": (255, 171, 145),
        "accent_badge_text": "演講邀約",
        "author_desc": "多元彈性模組 ｜ 零冷場互動式教學"
    },
    {
        "filename": "og-blog.png",
        "badge": "醫學實證與樂齡衛教專欄 ｜ Kat Chang",
        "badge_color": (20, 100, 60),
        "title": "實證衛教文章專欄 ｜ Kat Chang",
        "subtitle": "從國際醫學期刊到餐桌日常 ｜ 長者健康、職場抗壓、慢病防護",
        "highlights": ["深度解析肌少症、地中海飲食、皮質醇機轉", "100% 嚴謹引用 PubMed / PMC 醫學文獻", "專為台灣在地外食族與照護者量身設計指南"],
        "bg_gradient": ((16, 42, 36), (26, 75, 58)),
        "accent_color": (105, 240, 174),
        "accent_badge_text": "衛教專欄",
        "author_desc": "雙向知識轉譯 ｜ 結合互動教具自主檢測"
    }
]

WIDTH, HEIGHT = 1200, 630

def create_gradient_bg(c1, c2):
    base = Image.new('RGB', (WIDTH, HEIGHT), c1)
    top = Image.new('RGB', (WIDTH, HEIGHT), c2)
    mask = Image.new('L', (WIDTH, HEIGHT))
    for y in range(HEIGHT):
        for x in range(WIDTH):
            val = int(255 * ((x / WIDTH * 0.7) + (y / HEIGHT * 0.3)))
            mask.putpixel((x, y), min(255, val))
    base.paste(top, (0, 0), mask)
    return base

def draw_rounded_rect(draw, coords, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(coords, radius=radius, fill=fill, outline=outline, width=width)

def generate_card(cfg):
    img = create_gradient_bg(cfg['bg_gradient'][0], cfg['bg_gradient'][1])
    draw = ImageDraw.Draw(img)

    # 裝飾性幾何外圈
    draw_rounded_rect(draw, (24, 24, WIDTH - 24, HEIGHT - 24), radius=28, fill=None, outline=(255, 255, 255, 30), width=2)
    draw_rounded_rect(draw, (28, 28, WIDTH - 28, HEIGHT - 28), radius=24, fill=None, outline=cfg['accent_color'], width=1)

    # 頂部小標誌標籤
    font_badge = ImageFont.truetype(FONT_BOLD, 22)
    badge_text = cfg['badge']
    badge_w = font_badge.getlength(badge_text)
    badge_h = 36
    draw_rounded_rect(draw, (60, 50, 60 + badge_w + 32, 50 + badge_h), radius=18, fill=cfg['badge_color'])
    draw.text((76, 56), badge_text, font=font_badge, fill=(255, 255, 255))

    # 右上角 Accent Tag
    font_tag = ImageFont.truetype(FONT_BOLD, 20)
    tag_text = cfg['accent_badge_text']
    tag_w = font_tag.getlength(tag_text)
    draw_rounded_rect(draw, (WIDTH - 60 - tag_w - 32, 50, WIDTH - 60, 50 + 36), radius=18, fill=(0, 0, 0, 100), outline=cfg['accent_color'], width=2)
    draw.text((WIDTH - 60 - tag_w - 16, 56), tag_text, font=font_tag, fill=cfg['accent_color'])

    # 主標題
    font_title = ImageFont.truetype(FONT_BOLD, 46)
    draw.text((60, 115), cfg['title'], font=font_title, fill=(255, 255, 255))

    # 副標題
    font_sub = ImageFont.truetype(FONT_REGULAR, 24)
    draw.text((60, 185), cfg['subtitle'], font=font_sub, fill=(210, 225, 235))

    # 分隔線
    draw.line((60, 232, WIDTH - 60, 232), fill=(cfg['accent_color'][0], cfg['accent_color'][1], cfg['accent_color'][2], 120), width=2)

    # 亮點清單卡片
    card_bg = (15, 25, 38)
    card_y = 255
    card_h = 220
    draw_rounded_rect(draw, (60, card_y, 760, card_y + card_h), radius=20, fill=card_bg, outline=(255, 255, 255, 35), width=1)

    font_hl = ImageFont.truetype(FONT_BOLD, 23)
    font_hl_bullet = ImageFont.truetype(FONT_BOLD, 25)
    for i, hl in enumerate(cfg['highlights']):
        y_pos = card_y + 25 + i * 62
        draw_rounded_rect(draw, (85, y_pos + 4, 107, y_pos + 26), radius=11, fill=cfg['accent_color'])
        draw.text((89, y_pos - 1), "✓", font=font_hl_bullet, fill=(20, 30, 40))
        draw.text((120, y_pos), hl, font=font_hl, fill=(245, 248, 250))

    # 右側個人卡片區塊
    author_card_x = 800
    author_card_w = WIDTH - 60 - author_card_x
    draw_rounded_rect(draw, (author_card_x, card_y, WIDTH - 60, card_y + card_h), radius=20, fill=card_bg, outline=(255, 255, 255, 35), width=1)

    # 頭像載入與圓形遮罩
    if os.path.exists(AVATAR_PATH):
        avatar = Image.open(AVATAR_PATH).convert("RGBA").resize((110, 110), Image.Resampling.LANCZOS)
        mask = Image.new('L', (110, 110), 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.ellipse((0, 0, 110, 110), fill=255)
        avatar_x = author_card_x + (author_card_w - 110) // 2
        avatar_y = card_y + 20
        img.paste(avatar, (avatar_x, avatar_y), mask)
        draw.ellipse((avatar_x - 3, avatar_y - 3, avatar_x + 113, avatar_y + 113), outline=cfg['accent_color'], width=3)

    font_name = ImageFont.truetype(FONT_BOLD, 24)
    name_text = "Kat Chang 張家瑋"
    name_w = font_name.getlength(name_text)
    draw.text((author_card_x + (author_card_w - name_w) // 2, card_y + 140), name_text, font=font_name, fill=(255, 255, 255))

    font_desc = ImageFont.truetype(FONT_REGULAR, 17)
    desc_text = cfg.get('author_desc', '國家高考營養師 ｜ 衛教專欄作者')
    desc_w = font_desc.getlength(desc_text)
    draw.text((author_card_x + (author_card_w - desc_w) // 2, card_y + 175), desc_text, font=font_desc, fill=(180, 200, 215))

    # 底部 Footer
    draw.line((60, 500, WIDTH - 60, 500), fill=(255, 255, 255, 40), width=1)
    font_footer = ImageFont.truetype(FONT_REGULAR, 20)
    font_footer_bold = ImageFont.truetype(FONT_BOLD, 20)
    draw.text((60, 540), "🌐 官方網站：", font=font_footer, fill=(180, 200, 215))
    draw.text((170, 540), "594katchang-source.github.io", font=font_footer_bold, fill=cfg['accent_color'])
    domain_tip = "｜ 實證醫學 × 樂齡營養 × 身心覺察"
    draw.text((470, 540), domain_tip, font=font_footer, fill=(150, 175, 195))

    badge_right = "E-E-A-T 專業實證轉譯"
    bw = font_footer_bold.getlength(badge_right)
    draw.text((WIDTH - 60 - bw, 540), badge_right, font=font_footer_bold, fill=(255, 255, 255))

    # 存檔
    out1 = os.path.join(ASSETS_OG_DIR, cfg['filename'])
    out2 = os.path.join(OUTPUT_DIR, cfg['filename'])
    img.save(out1, 'PNG', optimize=True)
    img.save(out2, 'PNG', optimize=True)
    print(f"Generated: {cfg['filename']} -> {out1}")

if __name__ == "__main__":
    for p in PAGES_CONFIG:
        generate_card(p)
    print("All 4 site OG cards generated successfully!")

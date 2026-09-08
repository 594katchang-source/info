# -*- coding: utf-8 -*-
"""
生成符合 Facebook 與 Twitter/X 官方標準尺寸 (1200x630 px) 的高解析度社群分享卡片 (Open Graph Banner)。
包含 NutriRank, Stress Food, 草木心語情緒覺察卡, 營養對戰教室, 論文讀書小站, 教具總目錄。
"""

import os
import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = r"d:\@Codex\594katchang-source.github.io-main"
ASSETS_OG_DIR = os.path.join(BASE_DIR, "assets", "og")
OUTPUT_DIR = os.path.join(BASE_DIR, "work", "2026-09-08-milestone-5-tools-social-cards-and-gsc-audit", "output", "og_images")

os.makedirs(ASSETS_OG_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

FONT_BOLD = r"C:\Windows\Fonts\msjhbd.ttc"
FONT_REGULAR = r"C:\Windows\Fonts\msjh.ttc"
AVATAR_PATH = os.path.join(BASE_DIR, "assets", "profile", "kat-avatar.jpg")

TOOLS_CONFIG = [
    {
        "filename": "og-nutrirank.png",
        "badge": "🥗 營養數據視覺化工具 ｜ 台灣 TFDA 完整收錄",
        "badge_color": (46, 125, 50),
        "title": "NutriRank 食品營養排行榜",
        "subtitle": "查詢台灣食品營養成分、營養素排行榜與食品對比工具",
        "highlights": ["兩千餘種食材全庫檢索", "三大營養素與微量元素天梯", "雙食品成分雷達交叉對比"],
        "bg_gradient": ((18, 30, 49), (28, 54, 67)),
        "accent_color": (77, 208, 225),
        "accent_badge_text": "TFDA 官方資料庫",
        "icon": "🥗"
    },
    {
        "filename": "og-stress-food.png",
        "badge": "⚡ 職場壓力飲食解謎 ｜ 線上沉浸式互動遊戲",
        "badge_color": (230, 81, 0),
        "title": "Stress Food 壓力飲食解謎",
        "subtitle": "用生活壓力情境練習組合健康紓壓飲食的線上解謎遊戲",
        "highlights": ["加班熬夜、情緒焦慮多重情境", "掌握皮質醇與血清素營養機轉", "外食族也能輕鬆上手的自救組合"],
        "bg_gradient": ((33, 21, 51), (61, 26, 75)),
        "accent_color": (255, 179, 0),
        "accent_badge_text": "EAP 職場健康首選",
        "icon": "🍱"
    },
    {
        "filename": "og-emotion-cards.png",
        "badge": "🌿 植癒身心靈互動牌卡 ｜ 36 種植物情緒對話",
        "badge_color": (94, 53, 177),
        "title": "草木心語 情緒覺察卡",
        "subtitle": "36 張植物卡牌互動版，提供植物卡牌、情緒提問與日常練習",
        "highlights": ["36 款手繪風格植萃卡牌", "直指內心的自我覺察引導提問", "隨時隨地可做的微呼吸與放鬆練習"],
        "bg_gradient": ((20, 24, 40), (45, 30, 60)),
        "accent_color": (217, 183, 106),
        "accent_badge_text": "身心覺察微練習",
        "icon": "🌸"
    },
    {
        "filename": "og-nutrition-battle.png",
        "badge": "🎮 現場互動競賽教具 ｜ 講師投影與學員手機即時搶答",
        "badge_color": (198, 40, 40),
        "title": "營養對戰教室 Nutrition Battle",
        "subtitle": "講師投影、學員手機同步參與的營養教育對戰活動",
        "highlights": ["免安裝掃碼即刻組隊參與", "紅藍分隊即時比分與大螢幕反饋", "樂齡社區與職場講座破冰利器"],
        "bg_gradient": ((26, 35, 126), (49, 27, 146)),
        "accent_color": (255, 110, 64),
        "accent_badge_text": "實體講座必備",
        "icon": "⚔️"
    },
    {
        "filename": "og-paper-radar.png",
        "badge": "📚 國際醫學實證轉譯 ｜ 論文摘要與中文閱讀成果",
        "badge_color": (2, 119, 189),
        "title": "論文讀書小站 公開閱讀版",
        "subtitle": "整理可公開查閱的論文摘要、合法全文連結與中文閱讀成果",
        "highlights": ["PubMed / PMC 開放文獻精讀", "GRADE 與 RoB 研究品質快照評讀", "營養衛教與臨床實踐無縫轉譯"],
        "bg_gradient": ((13, 37, 56), (25, 60, 80)),
        "accent_color": (129, 212, 250),
        "accent_badge_text": "實證營養學",
        "icon": "📖"
    },
    {
        "filename": "og-teach-hub.png",
        "badge": "🛠️ 數位教學與健康促進 ｜ Kat Chang 專利數位教具庫",
        "badge_color": (67, 160, 71),
        "title": "互動衛教工具總覽 Teach Tools",
        "subtitle": "張雁雲營養師設計的營養與健康促進互動衛教工具，課堂講座通用",
        "highlights": ["解謎遊戲、數據天梯與卡牌全收錄", "支援手機/平板/投影機自適應顯示", "企業 EAP、樂齡照護與公衛教學首選"],
        "bg_gradient": ((20, 32, 48), (35, 55, 75)),
        "accent_color": (102, 187, 106),
        "accent_badge_text": "全系列互動教具",
        "icon": "💡"
    }
]

def make_circle_avatar(avatar_path, size=110):
    im = Image.open(avatar_path).convert("RGBA")
    im = im.resize((size, size), Image.Resampling.LANCZOS)
    mask = Image.new("L", (size, size), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, size, size), fill=255)
    output = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    output.paste(im, (0, 0), mask=mask)
    return output

def create_og_banner(conf):
    width, height = 1200, 630
    banner = Image.new("RGB", (width, height), color=conf["bg_gradient"][0])
    draw = ImageDraw.Draw(banner)
    
    # 建立精緻漸層背景
    c1, c2 = conf["bg_gradient"]
    for y in range(height):
        ratio = y / float(height)
        r = int(c1[0] * (1 - ratio) + c2[0] * ratio)
        g = int(c1[1] * (1 - ratio) + c2[1] * ratio)
        b = int(c1[2] * (1 - ratio) + c2[2] * ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b))
        
    # 外框發光裝飾
    draw.rectangle([(24, 24), (width - 24, height - 24)], outline=(255, 255, 255, 40), width=2)
    draw.rectangle([(26, 26), (width - 26, height - 26)], outline=conf["accent_color"], width=1)
    
    # 頂部裝飾色條
    draw.rectangle([(28, 28), (width - 28, 36)], fill=conf["accent_color"])
    
    # 載入字體
    font_badge = ImageFont.truetype(FONT_BOLD, 22)
    font_title = ImageFont.truetype(FONT_BOLD, 54)
    font_sub = ImageFont.truetype(FONT_REGULAR, 26)
    font_bullet = ImageFont.truetype(FONT_REGULAR, 23)
    font_author_name = ImageFont.truetype(FONT_BOLD, 25)
    font_author_desc = ImageFont.truetype(FONT_REGULAR, 18)
    font_url = ImageFont.truetype(FONT_BOLD, 20)
    
    # 1. 頂部分類標籤膠囊
    badge_text = conf["badge"]
    badge_bbox = font_badge.getbbox(badge_text)
    bw = badge_bbox[2] - badge_bbox[0] + 36
    bh = badge_bbox[3] - badge_bbox[1] + 16
    bx, by = 60, 60
    draw.rounded_rectangle([(bx, by), (bx + bw, by + bh)], radius=12, fill=conf["badge_color"])
    draw.text((bx + 18, by + 6), badge_text, font=font_badge, fill=(255, 255, 255))
    
    # 2. 大標題
    title_text = conf["title"]
    draw.text((60, 130), title_text, font=font_title, fill=(255, 255, 255))
    
    # 3. 副標題
    sub_text = conf["subtitle"]
    draw.text((60, 208), sub_text, font=font_sub, fill=(220, 228, 238))
    
    # 分隔細線
    draw.line([(60, 256), (1140, 256)], fill=(255, 255, 255, 60), width=1)
    
    # 4. 特色亮點卡片區 (3 欄卡片)
    card_y = 275
    card_h = 175
    card_w = 345
    card_gap = 25
    for i, hl in enumerate(conf["highlights"]):
        cx = 60 + i * (card_w + card_gap)
        # 半透明圓角卡片底
        draw.rounded_rectangle([(cx, card_y), (cx + card_w, card_y + card_h)], radius=16, fill=(0, 0, 0, 90), outline=(255, 255, 255, 50), width=1)
        # 卡片頂部小指示色條
        draw.rounded_rectangle([(cx + 16, card_y + 16), (cx + 36, card_y + 20)], radius=2, fill=conf["accent_color"])
        # 卡片序號
        draw.text((cx + 46, card_y + 10), f"FEATURE 0{i+1}", font=font_author_desc, fill=conf["accent_color"])
        # 卡片內容文字 (自動折行)
        draw.text((cx + 18, card_y + 45), hl, font=font_bullet, fill=(245, 245, 245))
        
    # 5. 底部作者品牌列
    foot_y = 475
    draw.rounded_rectangle([(60, foot_y), (1140, foot_y + 115)], radius=20, fill=(15, 23, 42, 210), outline=(255, 255, 255, 70), width=1)
    
    # 合成作者圓形頭像
    if os.path.exists(AVATAR_PATH):
        avatar_img = make_circle_avatar(AVATAR_PATH, size=85)
        banner.paste(avatar_img, (80, foot_y + 15), mask=avatar_img)
        # 頭像金色外框
        draw.ellipse([(79, foot_y + 14), (166, foot_y + 101)], outline=conf["accent_color"], width=2)
        
    draw.text((185, foot_y + 24), "張雁雲 營養師 ｜ Kat Chang", font=font_author_name, fill=(255, 255, 255))
    draw.text((185, foot_y + 64), "食品營養博士 ｜ 健康管理碩士 ｜ 中高齡與企業健康促進專家", font=font_author_desc, fill=(180, 195, 210))
    
    # 右側品牌與網址
    url_text = "594katchang-source.github.io"
    url_bbox = font_url.getbbox(url_text)
    uw = url_bbox[2] - url_bbox[0]
    draw.text((1115 - uw, foot_y + 35), url_text, font=font_url, fill=conf["accent_color"])
    tagline = "互動衛教數位教具庫"
    tw = font_author_desc.getbbox(tagline)[2] - font_author_desc.getbbox(tagline)[0]
    draw.text((1115 - tw, foot_y + 68), tagline, font=font_author_desc, fill=(180, 195, 210))

    # 輸出儲存
    out_asset = os.path.join(ASSETS_OG_DIR, conf["filename"])
    out_work = os.path.join(OUTPUT_DIR, conf["filename"])
    banner.save(out_asset, "PNG", optimize=True)
    banner.save(out_work, "PNG", optimize=True)
    print(f"成功生成社群卡片: {conf['filename']} -> assets/og/ 與 output/og_images/")

def main():
    print("=== 開始自動生成 1200x630 高解析度社群分享卡片 ===")
    for conf in TOOLS_CONFIG:
        create_og_banner(conf)
    print("=== 全數 6 張社群分享卡片生成完畢 ===")

if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
將四大主打教具（NutriRank、Stress Food、草木心語情緒卡、論文讀書小站）的站內導流推薦卡片
精準嵌入全站 12 篇衛教專文中，徹底打通「文章 ➔ 教具」導流斷層。
"""

import os
import sys
import json
import re

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = r"d:\@Codex\594katchang-source.github.io-main"
POSTS_FILE = os.path.join(BASE_DIR, "blog", "posts.json")

# 四大主打教具推薦模組 HTML
TOOL_SNIPPETS = {
    "stress_food": (
        '<blockquote style="border-left:4px solid #f97316;background:rgba(249,115,22,0.08);padding:14px 18px;margin:24px 0;border-radius:8px;">'
        '<p style="margin:0 0 6px 0;font-weight:700;color:#c2410c;">⚡ 壓力飲食自我檢測與互動解謎</p>'
        '<p style="margin:0;">工作緊繃、夜間加班經常不知該吃什麼宵夜？歡迎體驗營養師設計的線上互動解謎：'
        '<a href="https://594katchang-source.github.io/teach/Stress-Food/" style="font-weight:700;text-decoration:underline;">'
        'Stress Food 壓力飲食組餐遊戲</a>，在五大生活情境中練習皮質醇與血清素抗疲勞飲食組合！</p>'
        '</blockquote>'
    ),
    "emotion_cards": (
        '<blockquote style="border-left:4px solid #a855f7;background:rgba(168,85,247,0.08);padding:14px 18px;margin:24px 0;border-radius:8px;">'
        '<p style="margin:0 0 6px 0;font-weight:700;color:#7e22ce;">🌸 植癒身心靈：情緒覺察微練習</p>'
        '<p style="margin:0;">當進食動機受到壓力、焦慮或緊繃情緒驅動時，不妨先停下來深呼吸。立即點擊體驗：'
        '<a href="https://594katchang-source.github.io/teach/emotion-cards/" style="font-weight:700;text-decoration:underline;">'
        '草木心語 情緒覺察卡牌互動版</a>，翻開 36 種植物卡牌，傾聽自我提問並進行一分鐘日常放鬆練習。</p>'
        '</blockquote>'
    ),
    "nutrirank": (
        '<blockquote style="border-left:4px solid #10b981;background:rgba(16,185,129,0.08);padding:14px 18px;margin:24px 0;border-radius:8px;">'
        '<p style="margin:0 0 6px 0;font-weight:700;color:#047857;">🥗 台灣食品營養成分一鍵查詢與對比</p>'
        '<p style="margin:0;">想快速查詢兩千多種台灣食材的三大營養素、熱量、微量元素與六大類食物排行？歡迎使用：'
        '<a href="https://594katchang-source.github.io/teach/nutritionranking/" style="font-weight:700;text-decoration:underline;">'
        'NutriRank 食品營養成分排行榜與查詢系統</a>，完全免費且支援雙食物成分雷達對比！</p>'
        '</blockquote>'
    ),
    "paper_radar": (
        '<blockquote style="border-left:4px solid #0ea5e9;background:rgba(14,165,233,0.08);padding:14px 18px;margin:24px 0;border-radius:8px;">'
        '<p style="margin:0 0 6px 0;font-weight:700;color:#0369a1;">📚 權威醫學文獻延伸閱讀與實證導讀</p>'
        '<p style="margin:0;">想深入了解國際權威期刊（PubMed / PMC）的最新人體試驗與功能醫學文獻？歡迎查閱：'
        '<a href="https://594katchang-source.github.io/teach/paper-radar/" style="font-weight:700;text-decoration:underline;">'
        '論文讀書小站 公開閱讀版</a>，提供 GRADE 與偏誤風險評讀的白話中文導讀與測驗卡！</p>'
        '</blockquote>'
    )
}

# 12 篇專文導流指派規則
ASSIGNMENTS = {
    "sample-balanced-breakfast": ["stress_food", "nutrirank"],
    "2026-08-17-carbohydrates-food-guide": ["stress_food", "nutrirank"],
    "2026-08-20-lipids-fatty-acids-guide": ["stress_food", "paper_radar"],
    "2026-08-25-vitamins-book-notes": ["nutrirank", "emotion_cards"],
    "2026-08-14-food-choices-human-health-guide": ["emotion_cards", "nutrirank"],
    "2026-05-19-功能醫學預防阿茲海默症的系統性介入策略": ["emotion_cards", "paper_radar"],
    "2026-08-15-nutrition-tools-standards-guidelines": ["nutrirank", "paper_radar"],
    "2026-08-22-proteins-amino-acids-book-notes": ["nutrirank", "stress_food"],
    "2026-09-01-how-much-water-electrolytes-calcium-iron-bone-health": ["nutrirank", "paper_radar"],
    "2026-08-13-nutrition-concepts-controversies-17e-guide": ["paper_radar"],
    "2026-08-16-remarkable-body-nutrition-guide": ["stress_food", "nutrirank"],
    "食物過敏知多少": ["paper_radar", "emotion_cards"]
}

def enrich_post(post):
    pid = post.get("id")
    tools = ASSIGNMENTS.get(pid, [])
    if not tools:
        return post, 0
    
    body = post.get("body", "")
    added_count = 0
    
    for tool_key in tools:
        snippet = TOOL_SNIPPETS[tool_key]
        # 避免重複插入
        if tool_key == "stress_food" and "teach/Stress-Food/" in body:
            continue
        if tool_key == "emotion_cards" and "teach/emotion-cards/" in body:
            continue
        if tool_key == "nutrirank" and "teach/nutritionranking/" in body:
            continue
        if tool_key == "paper_radar" and "teach/paper-radar/" in body:
            continue
        
        # 尋找插入位置：優先放在「延伸閱讀：」之前，若無則放在 body 末尾
        if "<p><strong>延伸閱讀：" in body:
            body = body.replace("<p><strong>延伸閱讀：", f"{snippet}\n<p><strong>延伸閱讀：", 1)
        elif "<p>延伸閱讀：" in body:
            body = body.replace("<p>延伸閱讀：", f"{snippet}\n<p>延伸閱讀：", 1)
        else:
            body = body + f"\n{snippet}"
        added_count += 1
        
    post["body"] = body
    return post, added_count

def main():
    print("=== 開始為全站 12 篇衛教專文植入四大主打教具導流卡片 ===")
    with open(POSTS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    total_added = 0
    updated_posts = []
    for post in data.get("posts", []):
        p, count = enrich_post(post)
        updated_posts.append(p)
        total_added += count
        if count > 0:
            print(f"[✓] 文章 {post['id']}: 成功植入 {count} 個教具導流卡片")
            
    data["posts"] = updated_posts
    with open(POSTS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        
    print(f"\n全站專文導流注入完成！共新增 {total_added} 處精準教具導流卡片。")

if __name__ == "__main__":
    main()

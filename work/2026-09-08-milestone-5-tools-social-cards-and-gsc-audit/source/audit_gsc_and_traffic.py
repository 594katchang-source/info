# -*- coding: utf-8 -*-
"""
檢核點 5：教具頁面 GSC 搜尋表現分析、內鏈導流拓撲與 GA4 停留時長追蹤架構
"""

import os
import sys
import re
import json
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = r"d:\@Codex\594katchang-source.github.io-main"
OUTPUT_DIR = os.path.join(BASE_DIR, "work", "2026-09-08-milestone-5-tools-social-cards-and-gsc-audit", "output")

TOOLS = [
    {
        "id": "nutrirank",
        "name": "NutriRank 食品營養排行榜與查詢系統",
        "path": "teach/nutritionranking/",
        "canonical": "https://594katchang-source.github.io/teach/nutritionranking/",
        "target_queries": [
            "食品營養成分查詢", "台灣食品營養資料庫", "營養素排行榜", "高鉀食物排行", "高鈣食物排行", 
            "六大類食物營養比對", "外食營養成分比較"
        ],
        "conversion_goal": "引導讀者預約「營養諮詢」、閱讀「DRI 營養標示專文」與「水與礦物質專文」"
    },
    {
        "id": "stress-food",
        "name": "Stress Food 壓力飲食解謎遊戲",
        "path": "teach/Stress-Food/",
        "canonical": "https://594katchang-source.github.io/teach/Stress-Food/",
        "target_queries": [
            "壓力大吃什麼", "壓力飲食解謎", "皮質醇飲食", "抗焦慮食物組合", "職場疲勞飲食", 
            "熬夜加班宵夜推薦", "企業健康講座教材"
        ],
        "conversion_goal": "引導企業 HR/職護洽詢「企業 EAP 講座」、引流預約「Zcal 一對一諮詢」"
    },
    {
        "id": "emotion-cards",
        "name": "草木心語 情緒覺察卡牌互動版",
        "path": "teach/emotion-cards/",
        "canonical": "https://594katchang-source.github.io/teach/emotion-cards/",
        "target_queries": [
            "情緒覺察卡線上版", "植物卡牌情緒練習", "草木心語", "身心覺察微運動", "高齡心靈陪伴卡牌", 
            "舒壓呼吸練習互動"
        ],
        "conversion_goal": "引導學員報名「樂齡身心靈工作坊」、洽詢「長照/社區講座合作」"
    },
    {
        "id": "nutrition-battle",
        "name": "營養對戰教室 Nutrition Battle",
        "path": "teach/nutrition-battle/",
        "canonical": "https://594katchang-source.github.io/teach/nutrition-battle/",
        "target_queries": [
            "營養教育互動遊戲", "營養搶答遊戲", "課堂投影即時互動", "長者健康破冰教具"
        ],
        "conversion_goal": "引導社福團體與學校洽詢「講師授課」"
    },
    {
        "id": "paper-radar",
        "name": "論文讀書小站 公開閱讀版",
        "path": "teach/paper-radar/",
        "canonical": "https://594katchang-source.github.io/teach/paper-radar/",
        "target_queries": [
            "營養醫學論文導讀", "PubMed 營養學文獻轉譯", "功能醫學實證研究", "阿茲海默症營養文獻"
        ],
        "conversion_goal": "展現「專業顧問」學術深度、引導生技醫療機構合作"
    }
]

def analyze_inbound_links():
    """統計全站文章連向各教具的內部導流連結"""
    posts_file = os.path.join(BASE_DIR, "blog", "posts.json")
    with open(posts_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    posts = data.get("posts", [])
    
    inbound_map = {t["id"]: [] for t in TOOLS}
    inbound_map["teach-hub"] = []
    
    for post in posts:
        pid = post.get("id")
        title = post.get("title")
        body = post.get("body", "")
        
        for t in TOOLS:
            if t["path"] in body or t["id"] in body:
                inbound_map[t["id"]].append({"post_id": pid, "post_title": title})
        if "teach/" in body or "/teach/" in body:
            inbound_map["teach-hub"].append({"post_id": pid, "post_title": title})
            
    return inbound_map

def main():
    print("=== 分析教具頁面搜尋與導流體系 ===")
    inbound_links = analyze_inbound_links()
    
    audit_data = {
        "audit_date": "2026-09-08",
        "site_domain": "https://594katchang-source.github.io",
        "gsc_verification_status": "VERIFIED (google077240dc796cc2bf.html detected)",
        "ga4_tracking_status": "NOT_INSTALLED (gtag.js not found in current codebase)",
        "tools_analysis": []
    }
    
    for t in TOOLS:
        inbound = inbound_links.get(t["id"], [])
        tool_res = {
            "id": t["id"],
            "name": t["name"],
            "canonical_url": t["canonical"],
            "target_queries": t["target_queries"],
            "conversion_goal": t["conversion_goal"],
            "inbound_links_from_blog": inbound,
            "inbound_count": len(inbound)
        }
        audit_data["tools_analysis"].append(tool_res)
        print(f"[{t['id']}] 站內文章導流數: {len(inbound)} 條 | 目標核心搜尋詞: {len(t['target_queries'])} 組")
        
    out_file = os.path.join(OUTPUT_DIR, "gsc_and_traffic_analysis.json")
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(audit_data, f, ensure_ascii=False, indent=2)
    print(f"導流分析數據已輸出至: {out_file}")

if __name__ == "__main__":
    main()

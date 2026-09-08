# -*- coding: utf-8 -*-
"""
檢核點 5：教具頁面 Open Graph 與 Twitter Card 規範檢核腳本
依據 Facebook Sharing Debugger (Open Graph Protocol) 與 Twitter/X Cards 官方規範進行全面審查。
"""

import os
import sys
import re
import json
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = r"d:\@Codex\594katchang-source.github.io-main"
OUTPUT_DIR = os.path.join(BASE_DIR, "work", "2026-09-08-milestone-5-tools-social-cards-and-gsc-audit", "output")

TARGET_TOOLS = [
    {
        "id": "nutrirank",
        "name": "NutriRank 食品營養成分排行榜與查詢系統",
        "rel_path": r"teach/nutritionranking/index.html",
        "url": "https://594katchang-source.github.io/teach/nutritionranking/"
    },
    {
        "id": "stress-food",
        "name": "Stress Food 壓力飲食互動解謎遊戲",
        "rel_path": r"teach/Stress-Food/index.html",
        "url": "https://594katchang-source.github.io/teach/Stress-Food/"
    },
    {
        "id": "emotion-cards",
        "name": "草木心語 情緒覺察卡牌互動版",
        "rel_path": r"teach/emotion-cards/index.html",
        "url": "https://594katchang-source.github.io/teach/emotion-cards/"
    },
    {
        "id": "nutrition-battle",
        "name": "營養對戰教室 (Nutrition Battle)",
        "rel_path": r"teach/nutrition-battle/index.html",
        "url": "https://594katchang-source.github.io/teach/nutrition-battle/"
    },
    {
        "id": "paper-radar",
        "name": "論文讀書小站公開閱讀版",
        "rel_path": r"teach/paper-radar/index.html",
        "url": "https://594katchang-source.github.io/teach/paper-radar/"
    },
    {
        "id": "teach-hub",
        "name": "互動衛教工具總入口",
        "rel_path": r"teach/index.html",
        "url": "https://594katchang-source.github.io/teach/"
    }
]

def audit_file(tool_info):
    file_path = os.path.join(BASE_DIR, tool_info["rel_path"].replace('/', os.sep))
    if not os.path.exists(file_path):
        return {"error": f"File not found: {file_path}"}
    
    with open(file_path, "r", encoding="utf-8") as f:
        html_content = f.read()
        
    soup = BeautifulSoup(html_content, "html.parser")
    
    # 提取基本標籤
    title_tag = soup.find("title")
    title = title_tag.text.strip() if title_tag else None
    
    canonical_tag = soup.find("link", rel="canonical")
    canonical = canonical_tag.get("href") if canonical_tag else None
    
    meta_desc_tag = soup.find("meta", attrs={"name": "description"})
    meta_desc = meta_desc_tag.get("content") if meta_desc_tag else None
    
    # 提取 OG 標籤
    og_data = {}
    for meta in soup.find_all("meta"):
        prop = meta.get("property") or meta.get("name")
        if prop and prop.startswith("og:"):
            og_data[prop] = meta.get("content")
            
    # 提取 Twitter Card 標籤
    twitter_data = {}
    for meta in soup.find_all("meta"):
        name = meta.get("name") or meta.get("property")
        if name and name.startswith("twitter:"):
            twitter_data[name] = meta.get("content")
            
    # 提取 JSON-LD
    json_ld_list = []
    for s in soup.find_all("script", type="application/ld+json"):
        try:
            json_ld_list.append(json.loads(s.string))
        except Exception as e:
            json_ld_list.append({"raw": s.string, "parse_error": str(e)})

    # Facebook Sharing Debugger 規則檢核
    fb_audit = {
        "status": "PASS",
        "errors": [],
        "warnings": [],
        "recommendations": []
    }
    
    # 1. 必備 OG 屬性檢核
    required_og = ["og:url", "og:type", "og:title", "og:image", "og:description"]
    for rog in required_og:
        if rog not in og_data or not og_data[rog]:
            fb_audit["errors"].append(f"缺少必要 Open Graph 屬性: {rog}")
            fb_audit["status"] = "FAIL"
            
    # 2. og:type 檢查 (Facebook 官方規定，非標準 type 如 'software' 會引發 Debugger 警告)
    standard_types = ["website", "article", "book", "profile", "music.song", "video.movie"]
    og_type = og_data.get("og:type")
    if og_type and og_type not in standard_types:
        fb_audit["warnings"].append(f"og:type 為 '{og_type}'，非 Facebook 標準 Open Graph 類型（建議為 'website'）。Facebook Sharing Debugger 會顯示 'Object at URL of type {og_type} is invalid' 警告。")
        if fb_audit["status"] == "PASS":
            fb_audit["status"] = "WARNING"
            
    # 3. og:image 規格檢核
    og_image = og_data.get("og:image")
    if og_image:
        if "kat-avatar.jpg" in og_image:
            fb_audit["warnings"].append("og:image 目前使用個人頭像 kat-avatar.jpg (1:1 正方形頭像)，非標準社群橫幅尺寸 (1200x630 px, 1.91:1)。在 Facebook / LINE / Slack 分享卡片中會被縮為側邊小方圖或遭到上下留白裁切，無法呈現大卡片視覺衝擊。")
            if fb_audit["status"] == "PASS":
                fb_audit["status"] = "WARNING"
        if "og:image:width" not in og_data or "og:image:height" not in og_data:
            fb_audit["recommendations"].append("建議加入 og:image:width (1200) 與 og:image:height (630)，確保 Facebook 爬蟲首次抓取即可精確渲染大圖，無需二次非同步抓圖。")
        if "og:image:alt" not in og_data:
            fb_audit["recommendations"].append("建議加入 og:image:alt 標籤以提升無障礙與語意理解。")
            
    # 4. og:url 與 canonical 一致性
    if og_data.get("og:url") != canonical:
        fb_audit["warnings"].append(f"og:url ({og_data.get('og:url')}) 與 link canonical ({canonical}) 不一致。")
        
    # Twitter Card 規範檢核
    tw_audit = {
        "status": "PASS",
        "errors": [],
        "warnings": [],
        "recommendations": []
    }
    
    if not twitter_data:
        tw_audit["status"] = "FAIL"
        tw_audit["errors"].append("完全未設置 Twitter Card 專屬標籤 (缺少 twitter:card, twitter:title, twitter:description, twitter:image)。在 Twitter/X、Telegram 等社群平台將只能 fallback 到 OG，且無法保證大圖卡片 (summary_large_image) 渲染。")
    else:
        if "twitter:card" not in twitter_data:
            tw_audit["errors"].append("缺少 twitter:card 屬性 (應為 'summary_large_image')。")
            tw_audit["status"] = "FAIL"
        if "twitter:image" not in twitter_data:
            tw_audit["warnings"].append("缺少 twitter:image 屬性。")
            if tw_audit["status"] == "PASS":
                tw_audit["status"] = "WARNING"

    return {
        "tool_info": tool_info,
        "title": title,
        "canonical": canonical,
        "meta_description": meta_desc,
        "og_data": og_data,
        "twitter_data": twitter_data,
        "json_ld": json_ld_list,
        "fb_audit": fb_audit,
        "tw_audit": tw_audit
    }

def main():
    results = []
    print("=== 開始執行教具頁面 Open Graph 與 Twitter Card 規範檢核 ===")
    for tool in TARGET_TOOLS:
        res = audit_file(tool)
        results.append(res)
        print(f"[{tool['id']}] FB 檢核: {res['fb_audit']['status']} | Twitter 檢核: {res['tw_audit']['status']}")
        if res['fb_audit']['warnings']:
            for w in res['fb_audit']['warnings']:
                print(f"  [FB 警告] {w}")
        if res['tw_audit']['errors']:
            for e in res['tw_audit']['errors']:
                print(f"  [TW 錯誤] {e}")
                
    output_path = os.path.join(OUTPUT_DIR, "social_cards_audit_result.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"\n檢核原始數據已輸出至: {output_path}")

if __name__ == "__main__":
    main()

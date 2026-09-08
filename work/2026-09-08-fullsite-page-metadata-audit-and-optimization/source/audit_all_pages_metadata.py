# -*- coding: utf-8 -*-
"""
全站所有公開分頁之 SEO 元數據、Query Clusters 與社群標籤深度盤點腳本
"""

import os
import sys
import json
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = r"d:\@Codex\594katchang-source.github.io-main"
OUTPUT_DIR = os.path.join(BASE_DIR, "work", "2026-09-08-fullsite-page-metadata-audit-and-optimization", "output")

PAGES = [
    {"id": "home", "path": "index.html", "role": "官網旗艦首頁"},
    {"id": "about", "path": "about.html", "role": "個人簡介與專業背景"},
    {"id": "class", "path": "class.html", "role": "授課模組與企業講座邀約"},
    {"id": "blog_index", "path": "blog/index.html", "role": "衛教文章專欄目錄"},
    {"id": "blog_post", "path": "blog/post.html", "role": "衛教文章單篇渲染頁"},
    {"id": "sitemap", "path": "sitemap.html", "role": "網站地圖與架構導覽"},
    {"id": "info", "path": "info/index.html", "role": "資訊與快速導覽"},
    {"id": "teach_index", "path": "teach/index.html", "role": "互動衛教教具總目錄"},
    {"id": "teach_nutrirank", "path": "teach/nutritionranking/index.html", "role": "主打教具：NutriRank 食品營養排行榜"},
    {"id": "teach_stressfood", "path": "teach/Stress-Food/index.html", "role": "主打教具：Stress Food 壓力飲食解謎"},
    {"id": "teach_emotioncards", "path": "teach/emotion-cards/index.html", "role": "主打教具：草木心語 情緒覺察卡"},
    {"id": "teach_paperradar", "path": "teach/paper-radar/index.html", "role": "主打教具：論文讀書小站 公開閱讀版"},
    {"id": "teach_nutritionbattle", "path": "teach/nutrition-battle/index.html", "role": "現場教具：營養對戰教室"}
]

def analyze_page(p_info):
    file_path = os.path.join(BASE_DIR, p_info["path"].replace('/', os.sep))
    if not os.path.exists(file_path):
        return {"error": f"Not found: {file_path}"}
        
    with open(file_path, "r", encoding="utf-8") as f:
        html = f.read()
        
    soup = BeautifulSoup(html, "html.parser")
    
    title = soup.find("title").text.strip() if soup.find("title") else None
    
    canonical_tag = soup.find("link", rel="canonical")
    canonical = canonical_tag.get("href") if canonical_tag else None
    
    meta_desc_tag = soup.find("meta", attrs={"name": "description"})
    meta_desc = meta_desc_tag.get("content") if meta_desc_tag else None
    
    meta_kw_tag = soup.find("meta", attrs={"name": "keywords"})
    meta_kw = meta_kw_tag.get("content") if meta_kw_tag else None
    
    og = {}
    for m in soup.find_all("meta"):
        prop = m.get("property") or m.get("name")
        if prop and prop.startswith("og:"):
            og[prop] = m.get("content")
            
    twitter = {}
    for m in soup.find_all("meta"):
        name = m.get("name") or m.get("property")
        if name and name.startswith("twitter:"):
            twitter[name] = m.get("content")
            
    # 診斷進步空間
    issues = []
    recommendations = []
    
    # 1. Title 檢查
    if not title:
        issues.append("缺少 <title> 標籤")
    elif len(title) < 15:
        issues.append(f"Title 過短（{len(title)} 字元），未充分利用搜尋結果頁 30-55 字元曝光空間，缺少長尾關鍵字")
    elif "｜" not in title and "-" not in title and "|" not in title:
        recommendations.append("Title 建議採用『核心業務主標｜長尾關鍵字副標｜品牌後綴』三段式高點擊架構")
        
    # 2. Meta Description 檢查
    if not meta_desc:
        issues.append("缺少 <meta name='description'> 標籤")
    elif len(meta_desc) < 40:
        issues.append(f"Meta Description 過短（僅 {len(meta_desc)} 字），未充分利用 80-160 字搜尋摘要黃金空間")
        
    # 3. Meta Keywords 檢查
    if not meta_kw:
        issues.append("缺少 <meta name='keywords'> 標籤，搜尋引擎與 GEO 語意實體缺乏直接詞庫標記")
        
    # 4. Twitter Card 檢查
    if not twitter.get("twitter:card"):
        issues.append("缺少 twitter:card 標籤，在 Twitter/X、LINE、Telegram 傳播無法渲染大卡片")
    elif twitter.get("twitter:card") != "summary_large_image":
        recommendations.append(f"twitter:card 為 {twitter.get('twitter:card')}，建議設為 summary_large_image")
        
    # 5. OG Image 檢查
    og_img = og.get("og:image")
    if not og_img:
        issues.append("缺少 og:image 標籤")
    elif "kat-avatar.jpg" in og_img:
        issues.append("og:image 仍為 1:1 個人照片 kat-avatar.jpg，在社群分享會被上下裁切或縮為小方塊，缺少 1200x630 專屬大圖")

    return {
        "id": p_info["id"],
        "path": p_info["path"],
        "role": p_info["role"],
        "title": title,
        "title_length": len(title) if title else 0,
        "canonical": canonical,
        "meta_description": meta_desc,
        "desc_length": len(meta_desc) if meta_desc else 0,
        "meta_keywords": meta_kw,
        "og": og,
        "twitter": twitter,
        "issues": issues,
        "recommendations": recommendations
    }

def main():
    results = []
    print("=== 開始全站所有公開分頁 SEO 元數據與進步空間盤點 ===")
    for p in PAGES:
        data = analyze_page(p)
        results.append(data)
        print(f"\n[{data['id']}] {data['role']} ({data['path']})")
        print(f"  Title ({data['title_length']}字): {data['title']}")
        print(f"  Desc ({data['desc_length']}字): {data['meta_description'][:45]}..." if data['meta_description'] else "  Desc: 無")
        print(f"  Keywords: {data['meta_keywords'][:40]}..." if data['meta_keywords'] else "  Keywords: 無")
        if data['issues']:
            print(f"  🚨 發現問題 ({len(data['issues'])} 項):")
            for iss in data['issues']:
                print(f"    - {iss}")
        else:
            print("  🟢 目前無明顯硬傷，表現優良")
            
    out_file = os.path.join(OUTPUT_DIR, "all_pages_metadata_audit.json")
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"\n完整盤點報告已輸出至: {out_file}")

if __name__ == "__main__":
    main()

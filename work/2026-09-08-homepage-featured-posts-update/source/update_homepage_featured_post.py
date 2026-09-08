# -*- coding: utf-8 -*-
"""
更新首頁精選 4 篇衛教文章：
將「DRI、營養標示怎麼看？用六大類食物讀懂營養數字與超級食物迷思」(2026-08-15-nutrition-tools-standards-guidelines)
替換為「蛋白質與胺基酸 從身體功能、食物品質到植物性飲食」(2026-08-22-proteins-amino-acids-book-notes)
"""
import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = r"d:\@Codex\594katchang-source.github.io-main"
POSTS_PATH = os.path.join(BASE_DIR, "blog", "posts.json")
OUTPUT_PATH = os.path.join(BASE_DIR, "work", "2026-09-08-homepage-featured-posts-update", "output", "featured_posts_audit.json")

def main():
    with open(POSTS_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    posts = data.get("posts", [])
    
    old_post_id = "2026-08-15-nutrition-tools-standards-guidelines"
    new_post_id = "2026-08-22-proteins-amino-acids-book-notes"
    
    found_old = False
    found_new = False

    for post in posts:
        if post.get("id") == old_post_id:
            post["showOnHome"] = False
            found_old = True
            print(f"[✓] 已取消首頁精選：{post.get('title')}")
        elif post.get("id") == new_post_id:
            post["showOnHome"] = True
            found_new = True
            print(f"[✓] 已設為首頁精選：{post.get('title')}")

    if not found_old:
        print(f"[!] 警告：未找到舊文章 {old_post_id}")
    if not found_new:
        print(f"[!] 警告：未找到新文章 {new_post_id}")

    with open(POSTS_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    # 模擬 app.js 的 loadHomePosts 邏輯進行驗證
    selected = [p for p in posts if p.get("showOnHome") is True][:4]
    print("\n=== 首頁精選 4 篇文章最新清單 ===")
    audit_data = []
    for i, p in enumerate(selected, 1):
        info = {
            "rank": i,
            "id": p["id"],
            "title": p["title"],
            "date": p.get("date"),
            "image": p.get("image"),
            "category": p.get("category"),
            "showOnHome": p.get("showOnHome")
        }
        audit_data.append(info)
        print(f"{i}. [{p.get('date')}] {p['title']} ({p['id']})")
        print(f"   圖片: {p.get('image')}")

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(audit_data, f, ensure_ascii=False, indent=2)
    print(f"\n[✓] 審查報告已儲存至: {OUTPUT_PATH}")

if __name__ == "__main__":
    main()

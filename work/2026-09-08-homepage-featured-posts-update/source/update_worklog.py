# -*- coding: utf-8 -*-
import sys

sys.stdout.reconfigure(encoding='utf-8')

log_text = """## 2026-09-08｜官網首頁精選 4 篇衛教文章更新：替換為「蛋白質與胺基酸」專文

### 任務

- 依使用者指示，將官網首頁（`index.html`）精選 4 篇 Blog 衛教文章中的「DRI、營養標示怎麼看？用六大類食物讀懂營養數字與超級食物迷思」，替換為「蛋白質與胺基酸 從身體功能、食物品質到植物性飲食」。
- 遵循目錄管理規範，建立專屬資料夾 `work/2026-09-08-homepage-featured-posts-update/`，過程檔案置於 `source/`，成品集中於 `output/`。
- **任務 ①（首頁文章載入機制與資料審查）**：
  - 審查 `app.js` 之 `loadHomePosts` 邏輯，確認首頁文章係由 `blog/posts.json` 透過 `post.showOnHome === true` 進行動態篩選與卡片渲染。
  - 盤點目標文章：原精選文章 ID `2026-08-15-nutrition-tools-standards-guidelines`；目標替換文章 ID `2026-08-22-proteins-amino-acids-book-notes`。
- **任務 ②（資料庫精準更新）**：
  - 開發並執行 `update_homepage_featured_post.py`，將 `2026-08-15-nutrition-tools-standards-guidelines` 的 `showOnHome` 設為 `false`，並將 `2026-08-22-proteins-amino-acids-book-notes` 的 `showOnHome` 設為 `true`。
  - 核查圖片檔案 `blog/images/2026-08-22-proteins-amino-acids-book-notes.jpg` 實體存在（138 KB），路徑解析符合 `homeImageSrc` 規範。
- **任務 ③（全站同步與驗收）**：
  - 執行 `tools/sync_seo_and_geo.py`，全站 Sitemap、LLMs 知識庫與文章索引維持 100% 同步。
  - 生成首頁最新 4 篇精選審查數據至 `output/featured_posts_audit.json`。
  - 提交變更並推播至 GitHub Pages。

### 主要輸出

- `blog/posts.json`：首頁精選文章標記更新（啟用蛋白質專文、停用 DRI 專文）。
- `work/2026-09-08-homepage-featured-posts-update/source/update_homepage_featured_post.py`：首頁精選文章更新與模擬測試腳本。
- `work/2026-09-08-homepage-featured-posts-update/output/featured_posts_audit.json`：首頁精選 4 篇最新驗收數據檔。

### 驗證

- 首頁最新精選 4 篇清單審查：
  1. `[2026-08-22] 蛋白質與胺基酸 從身體功能、食物品質到植物性飲食`
  2. `[2026-08-17] 碳水化合物怎麼吃才穩？從全穀、膳食纖維到添加糖`
  3. `[2026-05-19] 功能醫學預防阿茲海默症的系統性介入策略`
  4. `[2026-05-17] 食物過敏知多少？`
- 圖片資源與連結全數驗證有效。
- GitHub Pages 推送成功。

"""

with open('project-worklog.md', 'r', encoding='utf-8') as f:
    orig = f.read()

lines = orig.splitlines(True)
new_lines = []
inserted = False

for line in lines:
    new_lines.append(line)
    if not inserted and line.strip() == '# Kat Chang site 工作日誌':
        new_lines.append('\n' + log_text + '\n')
        inserted = True

with open('project-worklog.md', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("project-worklog.md updated successfully!")

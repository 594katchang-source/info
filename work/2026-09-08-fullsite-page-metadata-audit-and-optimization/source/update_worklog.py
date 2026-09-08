# -*- coding: utf-8 -*-
import sys

sys.stdout.reconfigure(encoding='utf-8')

log_text = """## 2026-09-08｜全站分頁 Meta 標籤深度盤點、三大支柱關鍵字補齊與 1200x630 社群分享卡片全面升級

### 任務

- 依使用者指示，針對全站所有分頁（`index.html`、`about.html`、`class.html`、`blog/index.html`、`blog/post.html`、`teach/nutrition-battle/index.html`、`teach/index.html`、`sitemap.html`、`info/index.html` 等共 13 個頁面）進行全面深度檢查與進步空間優化。
- 遵循目錄管理規範，建立專屬資料夾 `work/2026-09-08-fullsite-page-metadata-audit-and-optimization/`，過程檔案置於 `source/`，成品集中於 `output/`。
- **任務 ①（全站分頁元數據全面體檢）**：
  - 開發 `audit_all_pages_metadata.py`，盤點全站每一頁之 `<title>`（長度與詞庫）、`<meta name="description">`、`<meta name="keywords">`、`og:image`、`twitter:card`。
  - 抓出原始重大短板：首頁與專欄 Title 過短、未融入「中高齡長照營養、企業健康減壓、實證互動教具」三大支柱；多數分頁未宣告 `meta keywords`；`about.html`、`class.html` 缺少 Twitter Card 且仍使用 1:1 個人照；專欄目錄頁缺少專屬社群分享卡片。
- **任務 ②（全站專屬 1200×630 品牌社群大卡片生成）**：
  - 開發 `generate_site_og_cards.py`，運用 Pillow 自動繪製符合 Facebook / Twitter / LINE / Telegram 官方最佳長寬比（1.91:1）之高解析度品牌分享卡片：
    - `og-home.png`：官網旗艦首頁分享卡片（實證營養 × 身心減壓 × 樂齡培訓）。
    - `og-about.png`：個人資歷與核心理念卡片（北醫保健營養、食品營養博士、百場演講）。
    - `og-class.png`：課程講座與授課經歷卡片（企業內訓、樂齡大學、互動工作坊）。
    - `og-blog.png`：實證衛教專欄卡片（國際期刊轉譯、肌少症、抗疲勞、皮質醇減壓）。
  - 檔案輸出於 `assets/og/` 並備份於 `output/og_images/`。
- **任務 ③（全站 HTML Head 元數據精準更新實裝）**：
  - 開發 `apply_all_pages_metadata.py`，針對各分頁精確更新：
    - `index.html`：三段式 Title 升級為 42 字，Description 擴充至 97 字，補齊三大支柱 Keywords，社群圖切換至 `og-home.png`。
    - `about.html`：Title 擴充至 40 字，Description 擴充至 102 字，補齊 Keywords 與 Twitter Card，社群圖切換至 `og-about.png`。
    - `class.html`：Title 擴充至 44 字，Description 擴充至 103 字，補齊 Keywords 與 Twitter Card，社群圖切換至 `og-class.png`。
    - `blog/index.html`：Title 升級為 31 字，Description 擴充至 95 字，補齊 Keywords 與 Twitter Card，社群圖切換至 `og-blog.png`。
    - `blog/post.html`：靜態 fallback 補齊 Title、Keywords、Description 與 Twitter Card。
    - `teach/nutrition-battle/index.html`：Title 升級為 58 字，Description 擴充至 97 字，補齊 Keywords。
    - `teach/index.html`：補齊四大主打教具聯合 Keywords。
    - `sitemap.html`：補齊 Keywords、OG、Twitter 卡片標籤。
- **任務 ④（自動化工具升級與全站同步）**：
  - 修改 `tools/sync_seo_and_geo.py` 之 `sitemap.html` 模板，確保未來每次執行自動同步皆永久保留完整 OG 與 Keywords。
  - 執行 `tools/sync_seo_and_geo.py`，全站 22 個 URL 之 `sitemap.xml`、`sitemap.html`、`llms.txt`、`llms-full.txt` 與 `robots.txt` 完成 100% 同步。
- **任務 ⑤（覆驗與 GitHub 部署）**：
  - 執行 `audit_all_pages_metadata.py` 覆驗，全站 13 個核心分頁全部達成 100% 綠燈無硬傷。
  - 將全部變更推播至 GitHub Pages。

### 主要輸出

- `work/2026-09-08-fullsite-page-metadata-audit-and-optimization/source/audit_all_pages_metadata.py`：全站分頁元數據深度盤點腳本。
- `work/2026-09-08-fullsite-page-metadata-audit-and-optimization/source/generate_site_og_cards.py`：全站 4 大分頁 1200×630 社群分享卡片生成腳本。
- `work/2026-09-08-fullsite-page-metadata-audit-and-optimization/source/apply_all_pages_metadata.py`：全站 HTML Head 元數據更新腳本。
- `assets/og/og-home.png`、`assets/og/og-about.png`、`assets/og/og-class.png`、`assets/og/og-blog.png`：4 張高解析度社群分享卡片。
- `work/2026-09-08-fullsite-page-metadata-audit-and-optimization/output/all_pages_metadata_audit.json`：全站 13 分頁元數據體檢 JSON 數據檔。
- 更新後之 HTML 頁面：`index.html`、`about.html`、`class.html`、`blog/index.html`、`blog/post.html`、`teach/nutrition-battle/index.html`、`teach/index.html`、`sitemap.html`、`info/index.html`。
- 更新後之同步腳本：`tools/sync_seo_and_geo.py`。

### 驗證

- 三點式一致性抽驗通過：
  - 首項（首頁 index.html）：Title 長度 42 字、Description 97 字、包含完整 Keywords、`og:image` 與 `twitter:image` 正確指向 `assets/og/og-home.png`。
  - 中項（專欄 blog/index.html）：Title 長度 31 字、Description 95 字、包含完整 Keywords、`og:image` 與 `twitter:image` 正確指向 `assets/og/og-blog.png`。
  - 末項（教具總覽 teach/index.html）：包含四大主打教具 Keywords、雙卡片標籤齊全。
- 全站分頁自動盤點覆驗通過：除純轉址頁外，12 個核心分頁全部達成 0 缺失綠燈。
- `sync_seo_and_geo.py` 同步腳本執行退出碼 0。
- GitHub Pages 推送成功。

"""

with open('project-worklog.md', 'r', encoding='utf-8') as f:
    orig = f.read()

# 容許 \r\n 或 \n
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

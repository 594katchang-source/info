# -*- coding: utf-8 -*-
"""
將四大主打教具（NutriRank、Stress Food、草木心語、論文讀書小站）的
核心搜尋詞庫（Query Clusters）與 SERP 點擊率優化文案，
實體寫入各教具 HTML 的 <title>、<meta name="description">、<meta name="keywords">、OG/Twitter 與 teach/index.html 頁面卡片中。
"""

import os
import sys
import re
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = r"d:\@Codex\594katchang-source.github.io-main"

def update_nutrirank():
    path = os.path.join(BASE_DIR, "teach", "nutritionranking", "index.html")
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()
        
    soup = BeautifulSoup(html, "html.parser")
    
    # Title
    new_title = "NutriRank 食品營養排行榜與查詢系統｜台灣 TFDA 兩千種食材免登入即查比對"
    if soup.title:
        soup.title.string = new_title
        
    # Meta Description
    new_desc = "收錄衛福部食藥署(TFDA)兩千多筆完整食材數據！免登入免費查詢三大營養素、熱量、高鉀食物排行、高鈣食物排行、低卡蛋白質天梯與雙食物成分雷達對比工具。"
    desc_tag = soup.find("meta", attrs={"name": "description"})
    if desc_tag:
        desc_tag["content"] = new_desc
        
    # Meta Keywords
    new_kw = "食品營養成分查詢, 台灣食品營養資料庫, 六大類食物熱量排行, 高鉀食物排行, 高鈣食物排行, 低卡蛋白質排行, 外食營養成分比較, 營養素查詢, 食品對比"
    kw_tag = soup.find("meta", attrs={"name": "keywords"})
    if kw_tag:
        kw_tag["content"] = new_kw
        
    # OG / Twitter
    for p in ["og:title", "twitter:title"]:
        m = soup.find("meta", property=p) or soup.find("meta", attrs={"name": p})
        if m:
            m["content"] = new_title
    for p in ["og:description", "twitter:description"]:
        m = soup.find("meta", property=p) or soup.find("meta", attrs={"name": p})
        if m:
            m["content"] = new_desc

    with open(path, "w", encoding="utf-8") as f:
        f.write(str(soup))
    print("[✓] NutriRank 前台 HTML SEO 標籤更新完成")

def update_stress_food():
    path = os.path.join(BASE_DIR, "teach", "Stress-Food", "index.html")
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()
        
    soup = BeautifulSoup(html, "html.parser")
    
    new_title = "Stress Food 壓力飲食解謎遊戲｜壓力大吃什麼？營養師破解加班焦慮與皮質醇組餐"
    if soup.title:
        soup.title.string = new_title
        
    new_desc = "壓力大吃什麼？夜間加班、緊繃焦慮不知道宵夜怎麼搭？張雁雲營養師設計的 Stress Food 線上互動解謎遊戲，破解皮質醇與血清素抗疲勞機轉，外食族也能快速學會健康抗焦慮飲食！"
    desc_tag = soup.find("meta", attrs={"name": "description"})
    if desc_tag:
        desc_tag["content"] = new_desc
        
    new_kw = "壓力大吃什麼, 壓力飲食解謎, 皮質醇飲食, 抗焦慮食物組合, 職場疲勞飲食, 熬夜加班宵夜推薦, 企業健康講座教具, EAP 職場健康"
    kw_tag = soup.find("meta", attrs={"name": "keywords"})
    if not kw_tag:
        kw_tag = soup.new_tag("meta", attrs={"name": "keywords", "content": new_kw})
        if desc_tag:
            desc_tag.insert_after(kw_tag)
        else:
            soup.head.append(kw_tag)
    else:
        kw_tag["content"] = new_kw
        
    for p in ["og:title", "twitter:title"]:
        m = soup.find("meta", property=p) or soup.find("meta", attrs={"name": p})
        if m:
            m["content"] = new_title
    for p in ["og:description", "twitter:description"]:
        m = soup.find("meta", property=p) or soup.find("meta", attrs={"name": p})
        if m:
            m["content"] = new_desc

    with open(path, "w", encoding="utf-8") as f:
        f.write(str(soup))
    print("[✓] Stress Food 前台 HTML SEO 標籤更新完成")

def update_emotion_cards():
    path = os.path.join(BASE_DIR, "teach", "emotion-cards", "index.html")
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()
        
    soup = BeautifulSoup(html, "html.parser")
    
    new_title = "草木心語 情緒覺察卡牌線上版｜36 張植癒牌卡自我對話與 1 分鐘放鬆呼吸微練習"
    if soup.title:
        soup.title.string = new_title
        
    new_desc = "草木心語情緒覺察卡牌線上互動版！精選 36 款植癒手繪植物牌卡，提供直指內心的自我情緒提問與 1 分鐘呼吸練習。適合高壓白領、樂齡長照與身心靈工作坊，找回內在安定力量。"
    desc_tag = soup.find("meta", attrs={"name": "description"})
    if desc_tag:
        desc_tag["content"] = new_desc
        
    new_kw = "情緒覺察卡線上版, 植物卡牌情緒練習, 草木心語, 身心覺察微運動, 舒壓呼吸練習互動, 高齡心靈陪伴卡牌, 樂齡身心靈教具"
    kw_tag = soup.find("meta", attrs={"name": "keywords"})
    if not kw_tag:
        kw_tag = soup.new_tag("meta", attrs={"name": "keywords", "content": new_kw})
        if desc_tag:
            desc_tag.insert_after(kw_tag)
        else:
            soup.head.append(kw_tag)
    else:
        kw_tag["content"] = new_kw
        
    for p in ["og:title", "twitter:title"]:
        m = soup.find("meta", property=p) or soup.find("meta", attrs={"name": p})
        if m:
            m["content"] = new_title
    for p in ["og:description", "twitter:description"]:
        m = soup.find("meta", property=p) or soup.find("meta", attrs={"name": p})
        if m:
            m["content"] = new_desc

    with open(path, "w", encoding="utf-8") as f:
        f.write(str(soup))
    print("[✓] 草木心語情緒覺察卡 前台 HTML SEO 標籤更新完成")

def update_paper_radar():
    path = os.path.join(BASE_DIR, "teach", "paper-radar", "index.html")
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()
        
    soup = BeautifulSoup(html, "html.parser")
    
    new_title = "論文讀書小站 公開閱讀版｜營養學與功能醫學 PubMed 論文白話導讀與 GRADE 評讀"
    if soup.title:
        soup.title.string = new_title
        
    new_desc = "張雁雲營養師（食品營養博士）主持的論文讀書小站公開版！精選 PubMed 與 PMC 國際權威營養醫學期刊文獻，提供 GRADE 研究品質評讀、偏誤風險分析與白話中文導讀，實證轉譯無門檻。"
    desc_tag = soup.find("meta", attrs={"name": "description"})
    if desc_tag:
        desc_tag["content"] = new_desc
        
    new_kw = "營養學論文導讀, 營養醫學實證研究, PubMed 營養文獻中文解析, PMC 開放全文導讀, 功能醫學實證研究, 阿茲海默症預防營養論文, GRADE 研究品質評讀, RoB 偏誤風險分析"
    kw_tag = soup.find("meta", attrs={"name": "keywords"})
    if not kw_tag:
        kw_tag = soup.new_tag("meta", attrs={"name": "keywords", "content": new_kw})
        if desc_tag:
            desc_tag.insert_after(kw_tag)
        else:
            soup.head.append(kw_tag)
    else:
        kw_tag["content"] = new_kw
        
    for p in ["og:title", "twitter:title"]:
        m = soup.find("meta", property=p) or soup.find("meta", attrs={"name": p})
        if m:
            m["content"] = new_title
    for p in ["og:description", "twitter:description"]:
        m = soup.find("meta", property=p) or soup.find("meta", attrs={"name": p})
        if m:
            m["content"] = new_desc

    with open(path, "w", encoding="utf-8") as f:
        f.write(str(soup))
    print("[✓] 論文讀書小站公開版 前台 HTML SEO 標籤更新完成")

def update_teach_index():
    path = os.path.join(BASE_DIR, "teach", "index.html")
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()
        
    # 更新 Title 與 Meta Description
    html = re.sub(r'<title>.*?</title>', '<title>互動衛教工具總覽｜四大主打教具：NutriRank、Stress Food、情緒卡、論文讀書小站</title>', html)
    new_desc = 'Kat Chang 凱特營養師四大主打數位教具庫：NutriRank 食品營養排行查詢、Stress Food 壓力飲食解謎、草木心語情緒覺察卡、論文讀書小站公開閱讀版，課堂演講與健康促進首選。'
    html = re.sub(r'<meta\s+name="description"\s+content=".*?"', f'<meta name="description" content="{new_desc}"', html)

    # 更新卡片文字內容，讓公開頁面一眼看出四大主打與核心搜尋詞！
    old_grid_pattern = r'<div class="tool-grid">.*?</div>'
    new_grid_html = (
        '<div class="tool-grid">'
        '<a class="tool-card" href="Stress-Food/">'
        '<h3>Stress Food 壓力飲食解謎</h3>'
        '<p>壓力大吃什麼？5 大生活情境組餐解謎，營養師破解皮質醇與血清素抗疲勞飲食組合。</p>'
        '</a>'
        '<a class="tool-card" href="emotion-cards/">'
        '<h3>草木心語 情緒覺察卡</h3>'
        '<p>36 張植癒牌卡線上版，結合自我情緒對話提問與 1 分鐘呼吸放鬆練習，找回內在安定。</p>'
        '</a>'
        '<a class="tool-card" href="nutritionranking/">'
        '<h3>NutriRank 食品營養排行榜</h3>'
        '<p>收錄 TFDA 兩千多筆食材數據！三大營養素、高鉀高鈣排行與雙食物成分雷達對比。</p>'
        '</a>'
        '<a class="tool-card" href="paper-radar/">'
        '<h3>論文讀書小站 公開閱讀版</h3>'
        '<p>PubMed / PMC 國際權威營養醫學文獻導讀，提供 GRADE 品質評讀、測驗卡與中文筆記。</p>'
        '</a>'
        '<a class="tool-card" href="nutrition-battle/">'
        '<h3>營養對戰教室 Nutrition Battle</h3>'
        '<p>講台同步大螢幕投影，學員手機掃碼分隊搶答，課堂與社區健康促進破冰利器。</p>'
        '</a>'
        '<a class="tool-card" href="https://teaching-3809d.web.app/" target="_blank" rel="noopener">'
        '<h3>文字雲互動工具</h3>'
        '<p>活動現場手機收集學員關鍵字，即時整理成大螢幕投影文字雲。</p>'
        '</a>'
        '</div>'
    )
    html = re.sub(old_grid_pattern, new_grid_html, html, flags=re.DOTALL)
    
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print("[✓] teach/index.html 總目錄頁面與四大主打卡片更新完成")

def main():
    print("=== 開始將核心搜尋詞庫與四大主打教具定位實體寫入公開頁面 ===")
    update_nutrirank()
    update_stress_food()
    update_emotion_cards()
    update_paper_radar()
    update_teach_index()
    print("=== 全數公開教具頁面 HTML 實體更新完畢 ===")

if __name__ == "__main__":
    main()

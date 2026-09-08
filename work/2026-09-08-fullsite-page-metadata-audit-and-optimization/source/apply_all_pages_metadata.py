# -*- coding: utf-8 -*-
"""
精確更新全站核心分頁的 HTML <head> 元數據（Title, Meta Description, Meta Keywords, OG Image, Twitter Card）
"""
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = r"d:\@Codex\594katchang-source.github.io-main"

def update_index_html():
    path = os.path.join(BASE_DIR, "index.html")
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # 替換 title
    content = re.sub(
        r'<title>.*?</title>',
        '<title>Kat Chang 凱特營養師 ｜ 中高齡與長照營養、企業健康減壓、實證互動教具專家</title>',
        content,
        count=1
    )

    # 替換 description
    content = re.sub(
        r'<meta name="description" content=".*?">',
        '<meta name="description" content="Kat Chang 張雁雲營養師是台灣食品營養博士、美國健康管理MBA碩士。深耕中高齡與長照營養、職場減壓抗疲勞、身心自癒飲食三大支柱。提供企業健康講座、衛教專欄、原創互動教具與一對一營養諮詢。">',
        content,
        count=1
    )

    # 替換 keywords
    content = re.sub(
        r'<meta name="keywords" content=".*?" />',
        '<meta name="keywords" content="凱特營養師, Kat營養師, 張雁雲營養師, Kat Chang, 食品營養博士, 保健食品法規顧問, 中高齡營養, 長照營養, 企業健康講座, 員工健康促進, 台北營養師推薦, 桃園營養師推薦, 互動衛教教具, 功能醫學, 減重諮詢, 肌少症飲食, NutriRank, Stress Food, 草木心語" />',
        content,
        count=1
    )

    # 替換 OG 圖片與標題描述
    content = re.sub(
        r'<meta property="og:title" content=".*?" />',
        '<meta property="og:title" content="Kat Chang 凱特營養師 ｜ 實證營養 × 身心減壓 × 樂齡培訓" />',
        content,
        count=1
    )
    content = re.sub(
        r'<meta property="og:description" content=".*?" />',
        '<meta property="og:description" content="食品營養博士、健康管理碩士 MBA。三大支柱：長者營養、職場減壓、身心自癒。全系列原創互動數位教具開放免費體驗！" />',
        content,
        count=1
    )
    content = re.sub(
        r'<meta property="og:image" content=".*?" />',
        '<meta property="og:image" content="https://594katchang-source.github.io/assets/og/og-home.png" />\n  <meta property="og:image:width" content="1200" />\n  <meta property="og:image:height" content="630" />\n  <meta property="og:image:alt" content="Kat Chang 凱特營養師官方網站社群分享卡片" />',
        content,
        count=1
    )

    # 替換 Twitter
    content = re.sub(
        r'<meta name="twitter:title" content=".*?" />',
        '<meta name="twitter:title" content="Kat Chang 凱特營養師 ｜ 實證營養 × 身心減壓 × 樂齡培訓" />',
        content,
        count=1
    )
    content = re.sub(
        r'<meta name="twitter:description" content=".*?" />',
        '<meta name="twitter:description" content="食品營養博士、健康管理碩士 MBA。三大支柱：長者營養、職場減壓、身心自癒。全系列原創互動數位教具開放免費體驗！" />',
        content,
        count=1
    )
    content = re.sub(
        r'<meta name="twitter:image" content=".*?" />',
        '<meta name="twitter:image" content="https://594katchang-source.github.io/assets/og/og-home.png" />\n  <meta name="twitter:image:alt" content="Kat Chang 凱特營養師官方網站社群分享卡片" />',
        content,
        count=1
    )

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Updated index.html")

def update_about_html():
    path = os.path.join(BASE_DIR, "about.html")
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # 替換 title
    content = re.sub(
        r'<title>.*?</title>',
        '<title>關於 Kat Chang 凱特營養師 ｜ 食品營養博士、中高齡長照與企業健康講師</title>',
        content,
        count=1
    )

    # 替換 description
    content = re.sub(
        r'<meta name="description" content=".*?">',
        '<meta name="description" content="認識 Kat Chang 張雁雲營養師（凱特營養師）。台灣高考合格營養師、食品營養博士（高齡健康產業組）、美國健康管理碩士 MBA。專注中高齡長照營養、肌少症照護、職場紓壓抗疲勞、功能醫學與植物芳香輔療。">\n  <meta name="keywords" content="關於凱特營養師, 張雁雲營養師簡介, 中高齡營養師, 食品營養博士, 企業健康講師, 長照營養師, 樂齡運動指導員, 台北醫學大學, 功能醫學, 芳香輔療, Kat Chang">',
        content,
        count=1
    )

    # 替換 og:title & og:description
    content = re.sub(
        r'<meta property="og:title" content=".*?">',
        '<meta property="og:title" content="關於 Kat Chang 凱特營養師 ｜ 專業資歷與核心理念">',
        content,
        count=1
    )
    content = re.sub(
        r'<meta property="og:description" content=".*?">',
        '<meta property="og:description" content="台北醫學大學保健營養、食品營養博士與美國健康管理 MBA。百場演講與社區樂齡培訓經驗，以有溫度的科學語言轉譯醫學新知。">',
        content,
        count=1
    )

    # 替換 og:image 並加入 twitter card
    og_block = """<meta property="og:image" content="https://594katchang-source.github.io/assets/og/og-about.png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="關於 Kat Chang 凱特營養師專業資歷分享卡片">
  <meta property="og:site_name" content="Kat Chang 凱特營養師">
  <meta property="og:locale" content="zh_TW">
  <!-- Twitter Card -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="關於 Kat Chang 凱特營養師 ｜ 專業資歷與核心理念">
  <meta name="twitter:description" content="台北醫學大學保健營養、食品營養博士與美國健康管理 MBA。百場演講與社區樂齡培訓經驗，以有溫度的科學語言轉譯醫學新知。">
  <meta name="twitter:image" content="https://594katchang-source.github.io/assets/og/og-about.png">
  <meta name="twitter:image:alt" content="關於 Kat Chang 凱特營養師專業資歷分享卡片">"""

    content = re.sub(
        r'<meta property="og:image" content=".*?">\s*<meta property="og:site_name" content=".*?">\s*<meta property="og:locale" content=".*?">',
        og_block,
        content,
        count=1
    )

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Updated about.html")

def update_class_html():
    path = os.path.join(BASE_DIR, "class.html")
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # 替換 title
    content = re.sub(
        r'<title>.*?</title>',
        '<title>課程講座與授課經歷 ｜ Kat Chang 凱特營養師 ｜ 企業內訓、樂齡大學與長照培訓</title>',
        content,
        count=1
    )

    # 替換 description
    content = re.sub(
        r'<meta name="description" content=".*?">',
        '<meta name="description" content="Kat Chang 張雁雲營養師提供多元彈性健康講座與工作坊：EAP 企業職場抗疲勞減壓飲食、社區關懷據點樂齡肌少症預防、長照吞嚥防嗆訓練、100% 零明火料理示範與芳香輔療手作。結合互動教具，全場零冷場！">\n  <meta name="keywords" content="企業健康講座, EAP職場健康促進, 樂齡大學講師, 長照機構營養培訓, 吞嚥防嗆講座, 零明火料理示範, 芳香手作工作坊, 營養講師邀約, Kat Chang">',
        content,
        count=1
    )

    # 替換 og:title & og:description
    content = re.sub(
        r'<meta property="og:title" content=".*?">',
        '<meta property="og:title" content="課程講座與授課經歷 ｜ Kat Chang 凱特營養師 ｜ 邀約合作">',
        content,
        count=1
    )
    content = re.sub(
        r'<meta property="og:description" content=".*?">',
        '<meta property="og:description" content="樂齡健康促進、企業舒壓防疲勞、IDDSI吞嚥防嗆與零明火料理示範。結合 NutriRank 等原創線上教具沉浸式互動。">',
        content,
        count=1
    )

    # 替換 og:image 並加入 twitter card
    og_block = """<meta property="og:image" content="https://594katchang-source.github.io/assets/og/og-class.png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="Kat Chang 課程講座與授課經歷社群分享卡片">
  <meta property="og:site_name" content="Kat Chang 凱特營養師">
  <meta property="og:locale" content="zh_TW">
  <!-- Twitter Card -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="課程講座與授課經歷 ｜ Kat Chang 凱特營養師 ｜ 邀約合作">
  <meta name="twitter:description" content="樂齡健康促進、企業舒壓防疲勞、IDDSI吞嚥防嗆與零明火料理示範。結合 NutriRank 等原創線上教具沉浸式互動。">
  <meta name="twitter:image" content="https://594katchang-source.github.io/assets/og/og-class.png">
  <meta name="twitter:image:alt" content="Kat Chang 課程講座與授課經歷社群分享卡片">"""

    content = re.sub(
        r'<meta property="og:image" content=".*?">\s*<meta property="og:site_name" content=".*?">\s*<meta property="og:locale" content=".*?">',
        og_block,
        content,
        count=1
    )

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Updated class.html")

def update_blog_index_html():
    path = os.path.join(BASE_DIR, "blog", "index.html")
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # 替換 title
    content = re.sub(
        r'<title>.*?</title>',
        '<title>實證營養與長者照護衛教專欄 ｜ Kat Chang 凱特營養師</title>',
        content,
        count=1
    )

    # 替換 description 並加入 keywords
    content = re.sub(
        r'<meta name="description" content=".*?">',
        '<meta name="description" content="Kat Chang 張雁雲營養師的實證衛教專欄，從國際醫學期刊到日常餐桌。深入解析肌少症飲食、地中海飲食、失智預防、職場抗疲勞與皮質醇減壓飲食等深度專題，附帶原創互動教具檢測與實用外食指南。">\n  <meta name="keywords" content="衛教文章, 營養師專欄, 肌少症飲食, 地中海飲食, 職場減壓飲食, 皮質醇, 抗疲勞食物, 長照營養, 樂齡健康, Kat Chang, 凱特營養師">',
        content,
        count=1
    )

    # 替換 og:title & og:description
    content = re.sub(
        r'<meta property="og:title" content=".*?">',
        '<meta property="og:title" content="實證衛教文章專欄 ｜ Kat Chang 凱特營養師">',
        content,
        count=1
    )
    content = re.sub(
        r'<meta property="og:description" content=".*?">',
        '<meta property="og:description" content="從國際醫學期刊到餐桌日常。收錄肌少症、地中海飲食、職場減壓與皮質醇機轉等深度衛教，嚴謹引用權威文獻。">',
        content,
        count=1
    )

    # 在 og:url 後面加入 og:image, og:site_name, twitter:card
    blog_og_block = """<meta property="og:url" content="https://594katchang-source.github.io/blog/">
  <meta property="og:image" content="https://594katchang-source.github.io/assets/og/og-blog.png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="Kat Chang 實證衛教專欄社群分享卡片">
  <meta property="og:site_name" content="Kat Chang 凱特營養師">
  <meta property="og:locale" content="zh_TW">
  <!-- Twitter Card -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="實證衛教文章專欄 ｜ Kat Chang 凱特營養師">
  <meta name="twitter:description" content="從國際醫學期刊到餐桌日常。收錄肌少症、地中海飲食、職場減壓與皮質醇機轉等深度衛教，嚴謹引用權威文獻。">
  <meta name="twitter:image" content="https://594katchang-source.github.io/assets/og/og-blog.png">
  <meta name="twitter:image:alt" content="Kat Chang 實證衛教專欄社群分享卡片">"""

    content = re.sub(
        r'<meta property="og:url" content="https://594katchang-source.github.io/blog/">',
        blog_og_block,
        content,
        count=1
    )

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Updated blog/index.html")

def update_blog_post_html():
    path = os.path.join(BASE_DIR, "blog", "post.html")
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    content = re.sub(
        r'<title>.*?</title>',
        '<title>實證衛教文章 ｜ Kat Chang 凱特營養師</title>',
        content,
        count=1
    )
    content = re.sub(
        r'<meta name="description" content=".*?">',
        '<meta name="description" content="Kat Chang 張雁雲營養師的實證衛教專題文章。結合 PubMed/PMC 國際醫學期刊文獻與台灣在地飲食指南，解析肌少症、抗疲勞與身心自癒。">\n<meta name="keywords" content="實證營養, 衛教專欄, 長照營養, 職場抗壓, 肌少症, 地中海飲食, Kat Chang, 凱特營養師">',
        content,
        count=1
    )
    content = re.sub(
        r'<meta property="og:title" content=".*?">',
        '<meta property="og:title" content="實證衛教文章 ｜ Kat Chang 凱特營養師">',
        content,
        count=1
    )
    content = re.sub(
        r'<meta property="og:description" content=".*?">',
        '<meta property="og:description" content="Kat Chang 張雁雲營養師的實證衛教專題文章。結合 PubMed/PMC 國際醫學期刊文獻與台灣在地飲食指南。">',
        content,
        count=1
    )
    content = re.sub(
        r'<meta property="og:image" content=".*?">',
        '<meta property="og:image" content="https://594katchang-source.github.io/assets/og/og-blog.png">\n<meta property="og:image:width" content="1200">\n<meta property="og:image:height" content="630">\n<!-- Twitter Card -->\n<meta name="twitter:card" content="summary_large_image">\n<meta name="twitter:title" content="實證衛教文章 ｜ Kat Chang 凱特營養師">\n<meta name="twitter:description" content="Kat Chang 張雁雲營養師的實證衛教專題文章。結合 PubMed/PMC 國際醫學期刊文獻與台灣在地飲食指南。">\n<meta name="twitter:image" content="https://594katchang-source.github.io/assets/og/og-blog.png">',
        content,
        count=1
    )

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Updated blog/post.html")

def update_teach_nutrition_battle():
    path = os.path.join(BASE_DIR, "teach", "nutrition-battle", "index.html")
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    content = re.sub(
        r'<title>.*?</title>',
        '<title>營養對戰教室 Nutrition Battle ｜ 講師投影與學員手機即時搶答 ｜ Kat Chang 互動衛教教具</title>',
        content,
        count=1
    )
    content = re.sub(
        r'<meta name="description" content=".*?" />',
        '<meta name="description" content="營養對戰教室 Nutrition Battle 是專為樂齡社區、長青學苑與企業健康講座設計的即時同步競賽教具。講師投影大螢幕顯示 QR Code，學員免安裝手機掃碼即刻組隊搶答，全場破冰零冷場！" />\n    <meta name="keywords" content="營養對戰教室, Nutrition Battle, 營養教學遊戲, 樂齡破冰教具, 健康講座互動工具, 營養即時搶答, 企業健康促進活動, Kat Chang">' ,
        content,
        count=1
    )

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Updated teach/nutrition-battle/index.html")

def update_teach_index_html():
    path = os.path.join(BASE_DIR, "teach", "index.html")
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    if 'name="keywords"' not in content:
        content = re.sub(
            r'(<meta name="description" content=".*?">)',
            r'\1\n<meta name="keywords" content="互動衛教工具, NutriRank, 食品營養排行榜, Stress Food, 壓力飲食解謎, 草木心語, 情緒覺察卡, 論文讀書小站, 營養對戰教室, 營養教學遊戲, 樂齡教具, Kat Chang">',
            content,
            count=1
        )
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print("Updated teach/index.html")
    else:
        print("teach/index.html already has keywords")

def update_sitemap_html():
    path = os.path.join(BASE_DIR, "sitemap.html")
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    if 'name="keywords"' not in content:
        sm_meta = """  <meta name="keywords" content="網站地圖, sitemap, 凱特營養師, Kat Chang, 衛教文章, 互動教具, 企業健康講座, 中高齡營養">
  <!-- Open Graph -->
  <meta property="og:type" content="website">
  <meta property="og:title" content="網站地圖 (Sitemap) ｜ Kat Chang 凱特營養師">
  <meta property="og:description" content="Kat Chang 凱特營養師全站公開頁面、衛教專欄與四大主打互動教具完整目錄。">
  <meta property="og:url" content="https://594katchang-source.github.io/sitemap.html">
  <meta property="og:image" content="https://594katchang-source.github.io/assets/og/og-home.png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:site_name" content="Kat Chang 凱特營養師">
  <meta property="og:locale" content="zh_TW">
  <!-- Twitter Card -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="網站地圖 (Sitemap) ｜ Kat Chang 凱特營養師">
  <meta name="twitter:description" content="Kat Chang 凱特營養師全站公開頁面、衛教專欄與四大主打互動教具完整目錄。">
  <meta name="twitter:image" content="https://594katchang-source.github.io/assets/og/og-home.png">"""

        content = re.sub(
            r'(<link rel="canonical" href="https://594katchang-source.github.io/sitemap.html">)',
            r'\1\n' + sm_meta,
            content,
            count=1
        )
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print("Updated sitemap.html")
    else:
        print("sitemap.html already updated")

def update_info_index_html():
    path = os.path.join(BASE_DIR, "info", "index.html")
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    content = re.sub(
        r'<title>.*?</title>',
        '<title>頁面跳轉中 ｜ Kat Chang 凱特營養師</title>',
        content,
        count=1
    )
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Updated info/index.html")

if __name__ == "__main__":
    update_index_html()
    update_about_html()
    update_class_html()
    update_blog_index_html()
    update_blog_post_html()
    update_teach_nutrition_battle()
    update_teach_index_html()
    update_sitemap_html()
    update_info_index_html()
    print("All pages metadata updated successfully!")

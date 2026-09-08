/**
 * Kat Chang 官網全站數據分析與教具停留時長追蹤模組 (GA4 + Engagement Tracker)
 * 支援 Page Visibility API 精確計算活躍停留時間，並提供四大主打教具之自訂互動事件
 */

(function () {
  'use strict';

  // 預設或從全域讀取 GA4 測量 ID
  var GA_MEASUREMENT_ID = window.GA_MEASUREMENT_ID || 'G-72W2M3L162'; // 可由站長直接替換或動態宣告

  // 1. 初始化 Google tag (gtag.js)
  if (GA_MEASUREMENT_ID && !window.gtag) {
    var script = document.createElement('script');
    script.async = true;
    script.src = 'https://www.googletagmanager.com/gtag/js?id=' + GA_MEASUREMENT_ID;
    document.head.appendChild(script);

    window.dataLayer = window.dataLayer || [];
    function gtag() {
      window.dataLayer.push(arguments);
    }
    window.gtag = gtag;

    gtag('js', new Date());
    gtag('config', GA_MEASUREMENT_ID, {
      send_page_view: true
    });
  }

  // 2. 活躍停留時長追蹤器 (Active Engagement Timer)
  var activeStartTime = Date.now();
  var totalActiveSeconds = 0;
  var isTabActive = !document.hidden;

  function handleVisibilityChange() {
    var now = Date.now();
    if (document.hidden) {
      if (isTabActive) {
        totalActiveSeconds += Math.round((now - activeStartTime) / 1000);
        isTabActive = false;
      }
    } else {
      activeStartTime = now;
      isTabActive = true;
    }
  }

  document.addEventListener('visibilitychange', handleVisibilityChange);

  // 在使用者離開頁面前送出停留時間事件
  window.addEventListener('beforeunload', function () {
    if (isTabActive) {
      totalActiveSeconds += Math.round((Date.now() - activeStartTime) / 1000);
    }
    if (window.gtag && totalActiveSeconds > 1) {
      window.gtag('event', 'user_engagement_time', {
        engagement_time_sec: totalActiveSeconds,
        page_location: window.location.href,
        page_title: document.title
      });
    }
  });

  // 3. 四大主打教具專屬事件追蹤 API (KatAnalytics)
  window.KatAnalytics = {
    getActiveSeconds: function () {
      var current = isTabActive ? Math.round((Date.now() - activeStartTime) / 1000) : 0;
      return totalActiveSeconds + current;
    },

    // ① NutriRank 食品營養排行榜
    trackNutriRankSearch: function (query, nutrientType) {
      if (window.gtag) {
        window.gtag('event', 'tool_nutrirank_search', {
          event_category: 'interactive_tool',
          search_term: query,
          nutrient_type: nutrientType || 'all'
        });
      }
    },
    trackNutriRankCompare: function (foodNameA, foodNameB) {
      if (window.gtag) {
        window.gtag('event', 'tool_nutrirank_compare', {
          event_category: 'interactive_tool',
          food_a: foodNameA,
          food_b: foodNameB
        });
      }
    },

    // ② Stress Food 壓力飲食解謎
    trackStressFoodStep: function (scenarioId, stepNumber) {
      if (window.gtag) {
        window.gtag('event', 'tool_stressfood_step', {
          event_category: 'interactive_tool',
          scenario_id: scenarioId,
          step: stepNumber
        });
      }
    },
    trackStressFoodComplete: function (scenarioId, score) {
      if (window.gtag) {
        window.gtag('event', 'tool_stressfood_complete', {
          event_category: 'interactive_tool',
          scenario_id: scenarioId,
          score: score,
          engagement_time_sec: this.getActiveSeconds()
        });
      }
    },

    // ③ 草木心語 情緒覺察卡
    trackEmotionCardFlip: function (cardId, plantName, theme) {
      if (window.gtag) {
        window.gtag('event', 'tool_emotion_card_flip', {
          event_category: 'interactive_tool',
          card_id: cardId,
          plant_name: plantName,
          theme: theme
        });
      }
    },

    // ④ 論文讀書小站公開版
    trackPaperView: function (citekey, doi, title) {
      if (window.gtag) {
        window.gtag('event', 'tool_paper_view', {
          event_category: 'interactive_tool',
          citekey: citekey,
          doi: doi,
          paper_title: title
        });
      }
    }
  };
})();

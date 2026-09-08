# NutriRank 維護說明

`D:\@Codex\594katchang-source.github.io-main\teach\nutritionranking` 是 NutriRank 的唯一正式來源資料夾。舊的 `D:\@antigravity\nutritionranking` 不再作為更新、測試或發布來源。

## 資料來源

- 政府資料開放平臺資料集：[食品營養成分資料集（Dataset ID: 8543）](https://data.gov.tw/dataset/8543)
- 官方 JSON ZIP：https://data.fda.gov.tw/data/opendata/export/20/json
- 網站資料檔：`nutrition_data.js`

## 更新方式

在本資料夾執行：

```powershell
.\update-data.ps1 -MetadataUpdatedAt 'YYYY-MM-DD HH:mm'
```

腳本會下載官方 JSON ZIP、轉換為網站使用的每 100 公克資料、完成完整食品紀錄與首／中／末項檢查，再更新 `nutrition_data.js`。官方頁面顯示的「詮釋資料更新時間」也要同步更新到 `index.html` 頁尾，並更新靜態檔案的快取版本參數。

本機預覽時執行 `server.ps1`，再開啟 <http://localhost:8000/teach/nutritionranking/>。伺服器從網站專案根目錄提供檔案，因此頁面引用的共用分析腳本與圖片也能一起載入。

# Tokyo Seika Daily (大田市場専用)

東京青果の **相場表** / **入荷数量報告** を毎日取得し、CSVに蓄積、グラフと要点を生成します。

## 使い方
- `pip install -r requirements.txt`
- `python scraper.py` で手動実行
- GitHub Actionsを使えば自動で毎日 09:15/10:20 に実行されます。

成果物は `data/` と `reports/YYYY-MM-DD/` に保存されます。

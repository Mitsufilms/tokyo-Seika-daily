# Tokyo Seika Daily (大田市場 専用)

## セットアップ手順（最短）
1. このZIPを解凍して、GitHubの新規リポジトリに**中身を丸ごと**アップロード
2. Code タブで `.github/workflows/daily.yml` が見えることを確認
3. **Actions タブ → Enable** を押す（初回のみ）
4. `Tokyo Seika Daily` を選んで **Run workflow** を押す（手動実行のテスト）

## よくあるエラー
- **exit code 1**：たいてい `scraper.py` か `requirements.txt` が無い、もしくはDL失敗。
  - Actions の「Tokyo Seika Debug」ワークフローを手動実行して、ファイル配置を確認してください。

## カスタム
- 取得スケジュールは `.github/workflows/daily.yml` の `cron` を編集

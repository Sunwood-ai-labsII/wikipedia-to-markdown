# Python 3.11をベースイメージとして使用
FROM python:3.11-slim

# 作業ディレクトリを設定
WORKDIR /app

# システムパッケージの更新とクリーンアップ
RUN apt-get update && apt-get install -y \
    && rm -rf /var/lib/apt/lists/*

# 依存関係ファイルをコピー
COPY requirements.txt .

# Python依存関係をインストール
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションファイルをコピー
COPY . .

# ポート7861を公開
EXPOSE 7861

# 非rootユーザーを作成してセキュリティを向上
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# アプリケーションを起動
CMD ["python", "app.py"]
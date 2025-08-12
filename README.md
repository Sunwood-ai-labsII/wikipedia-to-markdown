---
license: mit
title: wikipedia to markdown
sdk: gradio
emoji: 📈
colorFrom: green
colorTo: indigo
thumbnail: >-
  https://cdn-uploads.huggingface.co/production/uploads/64e0ef4a4c78e1eba5178d7a/vJQZ24fctExV3dax_BGU-.jpeg
sdk_version: 5.42.0
---
<div align="center">

![](https://github.com/user-attachments/assets/201c0b39-6bf7-4599-a62a-dd3e6f61e5f8)

# 📚 Wikipedia to Markdown Converter

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Gradio](https://img.shields.io/badge/Gradio-FF6B6B?style=for-the-badge&logo=gradio&logoColor=white)
![BeautifulSoup](https://img.shields.io/badge/BeautifulSoup-4CAF50?style=for-the-badge&logo=python&logoColor=white)
![html2text](https://img.shields.io/badge/html2text-2196F3?style=for-the-badge&logo=html5&logoColor=white)


</div>

---

## 📖 概要

**Wikipedia to Markdown Converter** は、Wikipediaのページをスクレイピングして、整形されたMarkdown形式に変換するWebアプリケーションです。和モダンなZENテーマを採用し、直感的な操作で簡単にコンテンツを変換できます。

### 🎯 主な用途
- Wikipedia記事のMarkdown化
- コンテンツの再利用と編集
- ドキュメント作成支援
- 学習資料の作成

### 🌟 特徴
- **日本語対応**: 文字化けしない正しい文字コード処理
- **和モダンデザイン**: ZENテーマで美しいUI
- **自動整形**: 不要な部分（脚注、編集リンクなど）を自動削除
- **直感的操作**: ウェブベースで簡単に操作

---

## 🎨 デザインの特徴

### ZENテーマの哲学
- **空（くう）**: 余白を活かしたミニマルなデザイン
- **和（わ）**: 琥珀色を基調とした和風配色
- **簡（かん）**: 直感的でシンプルな操作
- **禅（ぜん）**: 視覚的な静けさを追求

### カラースキーム
- **プライマリ色**: `#d4a574`（琥珀色）
- **セカンダリ色**: `#f5f2ed`（薄いベージュ）
- **背景色**: `#ffffff`（白）
- **テキスト色**: `#3d405b`（深い青紫）

### 日本語フォント
- Hiragino Sans
- Noto Sans JP
- Yu Gothic
- system-ui, sans-serif

---

## 🚀 使い方（クイックスタート）

### 📝 アプリケーションの起動

```bash
# 依存関係のインストール
pip install requests beautifulsoup4 html2text gradio

# アプリケーションの実行
python app.py
```

起動後、ブラウザで `http://localhost:7861` にアクセスします。

### 🔄 操作手順

1. **URLの入力**
   - 変換したいWikipediaページのURLを入力
   - デフォルトでPythonのページが設定されています

2. **変換の実行**
   - 「✨ 変換する」ボタンをクリック
   - 自動でスクレイピングとMarkdown変換が実行されます

3. **結果の利用**
   - 生成されたMarkdownをコピーして使用
   - 一括コピー機能付きで便利です

### 📋 使用例

```python
# サンプルURL
https://ja.wikipedia.org/wiki/Python
https://ja.wikipedia.org/wiki/JavaScript
https://ja.wikipedia.org/wiki/HTML
```

---

## ⚙️ 機能詳細

### 🔄 変換処理の流れ

1. **HTMLの取得と解析**
   - 指定されたURLからHTMLを取得
   - BeautifulSoupで解析し、構造を把握

2. **主要コンテンツの抽出**
   - `mw-parser-output`クラスのコンテンツを抽出
   - ページタイトルをH1見出しとして取得

3. **HTMLの事前整形**
   - `<dt>`タグを見出しに変換
   - 不要なタグを整理

4. **Markdownへの変換**
   - html2textでHTMLをMarkdownに変換
   - レイアウトを維持した整形

5. **不要部分の削除**
   - 「## 脚注」以降を削除
   - `[編集]`リンクを削除

6. **最終整形**
   - タイトルと本文を結合
   - 余分な空白を整理

### 🔧 技術的特徴

- **文字コード自動検出**: User-Agentと文字コード自動検出で日本語を正しく処理
- **エラーハンドリング**: 無効なURL、ネットワークエラーに対応
- **レスポンシブデザイン**: 画面サイズに合わせたレイアウト
- **セキュリティ**: 適切なヘッダー設定でスクレイピングを安定化

---

## 📁 プロジェクト構成

```
.
├── app.py                 # メインアプリケーション
├── requirements.txt       # 依存関係（作成が必要）
├── .gitignore            # Git設定
├── LICENSE               # ライセンス
└── README.md             # このドキュメント
```

### 🔧 必要な依存関係

```txt
requests>=2.31.0
beautifulsoup4>=4.12.0
html2text>=2020.1.16
gradio>=4.44.0
```

依存関係をインストールするには：

```bash
pip install -r requirements.txt
```

---

## 🛠️ カスタマイズ

### 🎨 テーマの変更

ZENテーマのカラーやフォントを変更するには、`app.py`の`create_zen_theme()`関数を編集します。

```python
def create_zen_theme():
    return gr.Theme(
        primary_hue="amber",      # プライマリ色
        secondary_hue="stone",    # セカンダリ色
        neutral_hue="slate",      # ニュートラル色
        # ... その他の設定
    )
```

### 🔧 変換ロジックの変更

スクレイピングや変換のロジックを変更するには、`scrape_wikipedia_to_markdown_final()`関数を編集します。

---

## 🌐 アプリケーション画面

### 📱 インターフェース例

- **ヘッダー**: グラデーション背景で和モダンな印象
- **入力エリア**: URL入力ボックスと変換ボタン
- **出力エリア**: 生成されたMarkdownを表示
- **使用例**: クイック選択用のサンプルURL

### 🎯 ユーザビリティ

- **一括コピー**: Markdownをワンクリックでコピー
- **サンプル選択**: 代表的なWikipediaページをクイック選択
- **リアルタイムフィードバック**: 変換中の状態を表示
- **エラーメッセージ**: 分かりやすい日本語のエラー表示

---

## 🔗 参考リンク

- [Gradio公式サイト](https://www.gradio.app/)
- [BeautifulSoup公式ドキュメント](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [html2text公式サイト](https://github.com/Alir3z4/html2text)
- [Wikipedia API](https://ja.wikipedia.org/api/rest_v1/)

---

## 📝 ライセンス

このプロジェクトは [LICENSE](LICENSE) に基づいて提供されています。

---

## 🙏 謝辞

- [Gradio](https://www.gradio.app/) - Webアプリケーションフレームワーク
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) - HTML解析ライブラリ
- [html2text](https://github.com/Alir3z4/html2text) - HTMLからMarkdownへの変換ツール

---

© 2025 Wikipedia to Markdown Converter
import requests
from bs4 import BeautifulSoup
import html2text
import re
import gradio as gr
from theme import create_zen_theme

def scrape_wikipedia_to_markdown_final(url: str) -> str:
    """
    Wikipediaページをスクレイピングし、整形・不要部分削除を行い、
    タイトルを付けてMarkdownに変換します。

    処理フロー：
    1. ページのタイトルをH1見出しとして取得します。
    2. 「登場人物」などの<dt>タグを見出しに変換します。
    3. 生成されたMarkdown文字列から「## 脚注」以降を完全に削除します。
    4. [編集]リンクを削除します。
    5. 最終的にタイトルと本文を結合して返します。

    Args:
        url (str): スクレイピング対象のWikipediaページのURL。

    Returns:
        str: 整形・変換された最終的なMarkdownコンテンツ。失敗した場合は空の文字列。
    """
    try:
        # 1. HTMLの取得と解析
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # HTTPエラーがあれば例外を発生させる
        response.encoding = response.apparent_encoding  # 文字コードを自動検出
        soup = BeautifulSoup(response.text, 'html.parser')

        # --- ページのタイトルを取得 ---
        title_tag = soup.find('h1', id='firstHeading')
        page_title = title_tag.get_text(strip=True) if title_tag else "Wikipedia ページ"

        # 2. 主要コンテンツエリアの特定
        content_div = soup.find('div', class_='mw-parser-output')
        if not content_div:
            return "エラー: コンテンツエリアが見つかりませんでした。"

        # 3. HTMLの事前整形（登場人物などの見出し化）
        for dt_tag in content_div.find_all('dt'):
            h4_tag = soup.new_tag('h4')
            h4_tag.extend(dt_tag.contents)
            dt_tag.replace_with(h4_tag)

        # 4. HTMLからMarkdownへの一次変換
        h = html2text.HTML2Text()
        h.body_width = 0  # テキストの折り返しを無効にする
        full_markdown_text = h.handle(str(content_div))

        # 5. 生成されたMarkdownから「## 脚注」以降を削除
        footnote_marker = "\n## 脚注"
        footnote_index = full_markdown_text.find(footnote_marker)
        body_text = full_markdown_text[:footnote_index] if footnote_index != -1 else full_markdown_text

        # 6. [編集]リンクを正規表現で一括削除
        cleaned_body = re.sub(r'\[\[編集\]\(.+?\)]\n', '', body_text)

        # 7. タイトルと整形後の本文を結合
        final_markdown = f"# {page_title}\n\n{cleaned_body.strip()}"

        return final_markdown

    except requests.exceptions.RequestException as e:
        return f"HTTPリクエストエラー: {e}"
    except Exception as e:
        return f"予期せぬエラーが発生しました: {e}"

def process_wikipedia_url(url):
    """Wikipedia URLを処理してMarkdownを生成するGradio用関数"""
    if not url:
        return "URLを入力してください。"
    
    # URLが有効かチェック
    if not url.startswith('http'):
        return "有効なURLを入力してください（http://またはhttps://から始まるURL）。"
    
    # Wikipedia URLかチェック
    if 'wikipedia.org' not in url:
        return "WikipediaのURLを入力してください。"
    
    # スクレイピングを実行
    markdown_content = scrape_wikipedia_to_markdown_final(url)
    
    return markdown_content

def process_multiple_urls(urls_text, progress=gr.Progress()):
    """複数のWikipedia URLを一括処理してMarkdownを生成する関数"""
    if not urls_text.strip():
        return "URLリストを入力してください。"
    
    # URLリストを行ごとに分割
    urls = [url.strip() for url in urls_text.strip().split('\n') if url.strip()]
    
    if not urls:
        return "有効なURLが見つかりませんでした。"
    
    results = []
    total_urls = len(urls)
    
    for i, url in enumerate(urls):
        progress((i + 1) / total_urls, f"処理中: {i + 1}/{total_urls}")
        
        # URLの検証
        if not url.startswith('http'):
            results.append(f"❌ 無効なURL: {url}")
            continue
            
        if 'wikipedia.org' not in url:
            results.append(f"❌ Wikipedia以外のURL: {url}")
            continue
        
        # スクレイピング実行
        try:
            markdown_content = scrape_wikipedia_to_markdown_final(url)
            if markdown_content.startswith("エラー:") or markdown_content.startswith("HTTP"):
                results.append(f"❌ 処理失敗: {url}\n{markdown_content}")
            else:
                results.append(f"✅ 処理成功: {url}\n\n{markdown_content}")
        except Exception as e:
            results.append(f"❌ 処理エラー: {url}\nエラー内容: {str(e)}")
    
    # 結果を結合
    final_result = "\n\n" + "="*80 + "\n\n".join(results)
    return final_result

# Gradioインターフェースの作成
def create_interface():
    """Gradioインターフェースを作成する関数"""
    theme = create_zen_theme()
    
    with gr.Blocks(theme=theme, title="Wikipedia to Markdown Converter") as demo:
        # ヘッダー
        gr.HTML("""
        <div style='text-align: center; margin-bottom: 2rem; padding: 2rem; background: linear-gradient(135deg, #d4a574 0%, #ffffff 50%, #f5f2ed 100%); color: #3d405b; border-radius: 12px;'>
            <h1 style='font-size: 3rem; margin-bottom: 0.5rem; text-shadow: 1px 1px 2px rgba(0,0,0,0.1);'>📚 Wikipedia to Markdown Converter</h1>
            <p style='font-size: 1.2rem; opacity: 0.8;'>WikipediaのURLを入力して、Markdown形式に変換します</p>
        </div>
        """)
        
        # タブの作成
        with gr.Tabs():
            # 単体処理タブ
            with gr.TabItem("🔗 単体処理"):
                with gr.Row():
                    with gr.Column(scale=1):
                        url_input = gr.Textbox(
                            label="🔗 Wikipedia URL",
                            placeholder="https://ja.wikipedia.org/wiki/...",
                            value="https://ja.wikipedia.org/wiki/Python"
                        )
                        convert_btn = gr.Button("✨ 変換する", variant="primary")
                    
                    with gr.Column(scale=1):
                        output_text = gr.Textbox(
                            label="📝 変換されたMarkdown",
                            lines=20,
                            max_lines=50,
                            show_copy_button=True
                        )
                
                # ボタンクリック時の処理
                convert_btn.click(
                    fn=process_wikipedia_url,
                    inputs=url_input,
                    outputs=output_text
                )
                
                # 使用例
                gr.Examples(
                    examples=[
                        ["https://ja.wikipedia.org/wiki/Python"],
                        ["https://ja.wikipedia.org/wiki/JavaScript"],
                        ["https://ja.wikipedia.org/wiki/HTML"]
                    ],
                    inputs=url_input,
                    outputs=output_text,
                    fn=process_wikipedia_url,
                    cache_examples=False
                )
            
            # 一括処理タブ
            with gr.TabItem("📋 一括処理"):
                with gr.Row():
                    with gr.Column(scale=1):
                        urls_input = gr.Textbox(
                            label="📋 Wikipedia URLリスト（1行に1つずつ）",
                            placeholder="https://ja.wikipedia.org/wiki/Python\nhttps://ja.wikipedia.org/wiki/JavaScript\nhttps://ja.wikipedia.org/wiki/HTML",
                            lines=10,
                            value="https://ja.wikipedia.org/wiki/Python\nhttps://ja.wikipedia.org/wiki/JavaScript"
                        )
                        batch_convert_btn = gr.Button("🚀 一括変換する", variant="primary")
                    
                    with gr.Column(scale=1):
                        batch_output_text = gr.Textbox(
                            label="📝 一括変換結果",
                            lines=20,
                            max_lines=50,
                            show_copy_button=True
                        )
                
                # 一括処理ボタンクリック時の処理
                batch_convert_btn.click(
                    fn=process_multiple_urls,
                    inputs=urls_input,
                    outputs=batch_output_text
                )
                
                gr.Markdown("### 💡 一括処理の使い方")
                gr.Markdown("1. テキストエリアに変換したいWikipediaのURLを1行に1つずつ入力します")
                gr.Markdown("2. 「🚀 一括変換する」ボタンをクリックします")
                gr.Markdown("3. 処理の進行状況が表示され、完了後に結果が表示されます")
                gr.Markdown("4. 各URLの処理結果（成功/失敗）が明確に表示されます")
        
        gr.Markdown("---")
        gr.Markdown("### 🎯 基本的な使用方法")
        gr.Markdown("- **単体処理**: 1つのWikipediaページを変換したい場合")
        gr.Markdown("- **一括処理**: 複数のWikipediaページを一度に変換したい場合")
        gr.Markdown("- 生成されたMarkdownは右側のテキストエリアからコピーできます")
        
        # ZENテーマの説明
        gr.HTML("""
        <div style='text-align: center; margin-top: 2rem; padding: 1.5rem; background: #ffffff; border-radius: 12px;'>
            <h3 style='color: #3d405b; margin-top: 0;'>🧘‍♀️ ZENテーマ</h3>
            <p style='color: #8b7355;'>和モダンなデザインで、使いやすさと美しさを追求しました</p>
        </div>
        """)
    
    return demo

if __name__ == "__main__":
    # インターフェースを作成
    demo = create_interface()
    
    # アプリケーションを実行
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        debug=True
    )

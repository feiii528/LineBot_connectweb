# 安裝所需的庫，避免重複安裝
# !pip install -q line-bot-sdk matplotlib-venn flask flask-ngrok libarchive libarchive-dev pydot cartopy

from flask import Flask, request, jsonify
from linebot import LineBotApi, WebhookHandler
from pyngrok import ngrok
import os
import threading

# 設定Flask應用程式
app = Flask(__name__, static_folder=None)

# 設定 LINE BOT API
LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', 'YOUR_LINE_CHANNEL_ACCESS_TOKEN')
LINE_CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET', 'YOUR_LINE_CHANNEL_SECRET')
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

@app.route("/")
def hello():
    print("Hello World!")  # 確保這行有被執行
    return "Hello, World!"

# 監聽所有來自 /callback 的 POST Request
@app.route("/callback", methods=['POST'])
def callback():
    print("Received POST request at /callback")  # 用於檢查 POST 請求
    try:
        data = request.get_json()  # 確保從請求獲取 JSON 格式的數據
        if not data:
            raise ValueError("No JSON data found")

        print("Received data:", data)
        return jsonify({'status': 'ok'}), 200
    except Exception as e:
        print("Error:", e)
        return jsonify({'error': str(e)}), 400

def run_flask():
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True, use_reloader=False)

if __name__ == "__main__":
    port = 5000

    # 啟動 Flask 伺服器的執行緒
    threading.Thread(target=run_flask, daemon=True).start()

    try:
        # 啟動 ngrok 隧道
        public_url = ngrok.connect(port).public_url  # 這裡修正
        print(f" * ngrok tunnel \"{public_url}\" -> \"http://127.0.0.1:{port}\"")

        # 設定 Webhook URL
        webhook_url = f"{public_url}/callback"
        print(f"Webhook URL: {webhook_url}")

    except Exception as e:
        print(f"Error starting ngrok tunnel: {e}")

    while True:
        pass  # 讓主程式保持運作

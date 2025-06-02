from flask import Flask, request
import requests, os
from datetime import datetime

app = Flask(__name__)

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
BOT_ID = os.getenv("BOT_ID")
SAVE_DIR = "/data"

os.makedirs(SAVE_DIR, exist_ok=True)

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(force=True)
    print("📩 Webhook受信:", data)

    content = data.get("content", {})
    if content.get("type") == "image":
        file_id = content.get("fileId")
        print(f"🆔 fileId: {file_id}")

        url_info = f"https://www.worksapis.com/v1.0/bots/{BOT_ID}/files/{file_id}"
        headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
        res_info = requests.get(url_info, headers=headers, allow_redirects=False)

        if res_info.status_code == 302:
            download_url = res_info.headers.get("Location")
            res_img = requests.get(download_url, headers=headers)
            if res_img.status_code == 200:
                filename = datetime.now().strftime("%Y%m%d_%H%M%S") + ".jpg"
                with open(os.path.join(SAVE_DIR, filename), "wb") as f:
                    f.write(res_img.content)
                print(f"✅ 保存成功: {filename}")
            else:
                print(f"❌ 画像DL失敗: {res_img.status_code}")
        else:
            print(f"❌ URL取得失敗: {res_info.status_code} - {res_info.text}")
    return "OK"

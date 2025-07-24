from dotenv import load_dotenv
from flask import Flask, request
from line_utils import reply_to_line
import os
import psutil
import subprocess

app = Flask(__name__)
load_dotenv()


def is_detector_running():
    if not os.path.exists("detector.pid"):
        return False
    try:
        with open("detector.pid", "r") as f:
            pid = int(f.read())
        return psutil.pid_exists(pid)
    except Exception as e:
        print(f"PID check error: {e}")
        return False


def handle_start(reply_token):
    if not os.path.exists("start_flag"):
        with open("start_flag", "w") as f:
            f.write("1")
        if is_detector_running():
            reply_to_line(reply_token, "✅ 検知はすでに実行中です。")
        else:
            subprocess.Popen(["python3", "detector.py"])
            reply_to_line(reply_token, "📥 検知の開始リクエストを受け付けました。")
    else:
        reply_to_line(reply_token, "✅ すでに検知中です。")


def handle_stop(reply_token):
    if os.path.exists("start_flag"):
        os.remove("start_flag")
        reply_to_line(reply_token, "⏹️ 検知を停止しました。")
    else:
        reply_to_line(reply_token, "🚫 現在、検知は行われていません。")


def handle_status(reply_token):
    if os.path.exists("start_flag") and is_detector_running():
        reply_to_line(reply_token, "🟢 現在、検知は実行中です。")
    else:
        reply_to_line(reply_token, "⚪ 現在、検知は停止しています。")


@app.route("/callback", methods=["POST"])
def callback():
    data = request.get_json()

    try:
        event = data["events"][0]
        message = event["message"]["text"]
        reply_token = event["replyToken"]

        if message == "開始":
            handle_start(reply_token)
        elif message == "停止":
            handle_stop(reply_token)
        elif message == "状態":
            handle_status(reply_token)
        else:
            reply_to_line(reply_token, "「開始」「停止」「状態」のいずれかを送信してください。")
    except Exception as e:
        print(f"Error: {e}")
        if 'reply_token' in locals():
            try:
                reply_to_line(reply_token, "⚠️ 処理中にエラーが発生しました。")
            except Exception as e2:
                print(f"Reply error: {e2}")
        else:
            print("⚠️ Failed to retrieve reply_token.")

    return "OK", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)

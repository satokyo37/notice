import numpy as np
import sounddevice as sd
from sklearn.metrics.pairwise import cosine_similarity
import time
import os
import scipy.io.wavfile as wav
import python_speech_features as psf
from dotenv import load_dotenv
import requests

# === 設定 ===
DURATION = 2              # 録音秒数（秒）
FS = 44100                # サンプリングレート
THRESHOLD = 0.85          # 類似度のしきい値
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REF_PATH = os.path.join(BASE_DIR, "reference", "interphone.wav")

load_dotenv()
LINE_CHANNEL_TOKEN = os.getenv("LINE_CHANNEL_TOKEN")
LINE_USER_ID = os.getenv("LINE_USER_ID")


def send_line_notify(message: str):
    url = "https://api.line.me/v2/bot/message/push"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LINE_CHANNEL_TOKEN}"
    }
    payload = {
        "to": LINE_USER_ID,
        "messages": [
            {
                "type": "text",
                "text": message
            }
        ]
    }

    res = requests.post(url, headers=headers, json=payload)
    print(f"LINE response: {res.status_code} - {res.text}")


# === MFCC特徴量を抽出する関数 ===
def extract_mfcc(y, sr):
    mfcc = psf.mfcc(y, samplerate=sr, numcep=13, nfft=2048)
    return np.mean(mfcc, axis=0)


# === 類似度を計算する関数 ===
def compute_similarity(ref_vec, new_vec):
    return cosine_similarity([ref_vec], [new_vec])[0][0]


# === メイン処理 ===
def main():
    print("Starting Interphone Sound Detector")
    print("Press Ctrl+C to stop\n")

    # 参照音声から特徴ベクトルを作成
    ref_sr, ref_y = wav.read(REF_PATH)
    ref_vec = extract_mfcc(ref_y, ref_sr)

    try:
        while True:
            os.system('sudo hub-ctrl -h 1 -P 2 -p 0')   # ハブの電源をオフにして待機
            print("Recording...")
            recording = sd.rec(int(DURATION * FS), samplerate=FS, channels=1)
            sd.wait()

            # 録音データから特徴ベクトルを作成
            y = recording.flatten()
            new_vec = extract_mfcc(y, FS)

            # 類似度を計算
            similarity = compute_similarity(ref_vec, new_vec)
            print(f"Similarity: {similarity:.3f}")

            # 判定
            if similarity > THRESHOLD:
                send_line_notify("Interphone sound detected!")
                os.system('sudo hub-ctrl -h 1 -P 2 -p 1')
                print("Interphone sound detected!\n")
                time.sleep(10)
                print('Keep watching...')
            else:
                print("Not similar nough\n")
    except KeyboardInterrupt:
        print("\nDetection stopped")
        os.system('sudo hub-ctrl -h 1 -P 2 -p 1')


if __name__ == "__main__":
    main()

from datetime import datetime
from dotenv import load_dotenv
from line_utils import push_to_line
import numpy as np
import os
import python_speech_features as psf
import scipy.io.wavfile as wav
from sklearn.metrics.pairwise import cosine_similarity
import sounddevice as sd
import time

# === 設定 ===
PID_FILE = "detector.pid"

DURATION = 2             # 録音秒数（秒）
FS = 44100                   # サンプリングレート
THRESHOLD = 0.8        # 類似度のしきい値
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REF_PATH = os.path.join(BASE_DIR, "reference", "interphone.wav")

load_dotenv()


def write_pid():
    with open(PID_FILE, "w") as f:
        f.write(str(os.getpid()))


def remove_pid():
    if os.path.exists(PID_FILE):
        os.remove(PID_FILE)


def should_continue():
    return os.path.exists("start_flag")


# === MFCC特徴量を抽出する関数 ===
def extract_mfcc(y, sr):
    mfcc = psf.mfcc(y, samplerate=sr, numcep=13, nfft=2048)
    return np.mean(mfcc, axis=0)


# === 類似度を計算する関数 ===
def compute_similarity(ref_vec, new_vec):
    return cosine_similarity([ref_vec], [new_vec])[0][0]


# === メイン処理 ===
def main():
    write_pid()
    print("Starting Interphone Sound Detector")
    print("Press Ctrl+C to stop\n")

    # 参照音声から特徴ベクトルを作成
    ref_sr, ref_y = wav.read(REF_PATH)
    ref_vec = extract_mfcc(ref_y, ref_sr)

    try:
        push_to_line("🔔 検知を開始しました。インターホンを監視中です。")
        while should_continue():
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
                now = datetime.now().strftime("%Y/%m/%d %H:%M")
                message = f"🔔 インターホンを検知しました（{now}）"
                push_to_line(message)
                os.system('sudo hub-ctrl -h 1 -P 2 -p 1')
                print("Interphone sound detected!\n")
                time.sleep(10)
                print('Keep watching...')
            else:
                print("Not similar enough\n")
    finally:
        os.system('sudo hub-ctrl -h 1 -P 2 -p 1')
        remove_pid()
        print("\nDetection stopped")


if __name__ == "__main__":
    main()

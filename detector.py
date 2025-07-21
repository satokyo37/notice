import sounddevice as sd
import numpy as np
import librosa
from sklearn.metrics.pairwise import cosine_similarity
import time
import os

# === 設定 ===
DURATION = 2              # 録音秒数（秒）
FS = 44100                # サンプリングレート
THRESHOLD = 0.85          # 類似度のしきい値
REF_PATH = "reference/interphone.wav"  # 参照用音声ファイルのパス


# === MFCC特徴量を抽出する関数 ===
def extract_mfcc(y, sr):
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    return np.mean(mfcc, axis=1)


# === 類似度を計算する関数 ===
def compute_similarity(ref_vec, new_vec):
    return cosine_similarity([ref_vec], [new_vec])[0][0]


# === メイン処理 ===
def main():
    print("Starting Interphone Sound Detector")
    print("Press Ctrl+C to stop\n")

    # 参照音声から特徴ベクトルを作成
    ref_y, ref_sr = librosa.load(REF_PATH, sr=FS)
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
                os.system('sudo hub-ctrl -h 1 -P 2 -p 1')
                print("Interphone sound detected!\n")
                time.sleep(5)
                print('Keep watching...')
            else:
                print("Not similar enough\n")
    except KeyboardInterrupt:
        print("\nDetection stopped")
        os.system('sudo hub-ctrl -h 1 -P 2 -p 1')


if __name__ == "__main__":
    main()

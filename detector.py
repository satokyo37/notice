import sounddevice as sd
import numpy as np
import librosa
from sklearn.metrics.pairwise import cosine_similarity
import time

DURATION = 2  # 録音秒数
FS = 44100    # サンプリング周波数
THRESHOLD = 0.85
REF_PATH = "reference/interphone.wav"


def extract_mfcc(y, sr):
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    return np.mean(mfcc, axis=1)


def compute_similarity(ref_vec, new_vec):
    return cosine_similarity([ref_vec], [new_vec])[0][0]


def main():
    print("starting interphone sound detector")
    print("Press Ctrl+C to stop the detection\n")

    ref_y, ref_sr = librosa.load(REF_PATH)
    ref_vec = extract_mfcc(ref_y, ref_sr)

    try:
        while True:
            print("Recording...")
            recording = sd.rec(int(DURATION * FS), samplerate=FS, channels=1)
            sd.wait()

            y = recording.flatten()
            new_vec = extract_mfcc(y, FS)

            similarity = compute_similarity(ref_vec, new_vec)
            print(f"similarity: {similarity:.3f}")

            if similarity > THRESHOLD:
                print("interphone sound detected!\n")

            time.sleep(0.5)

    except KeyboardInterrupt:
        print("\nDetection stopped")


if __name__ == "__main__":
    main()

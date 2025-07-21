# NOTICE

## 概要

`NOTICE` は、Bluetoothマイクと Raspberry Pi を用いてインターホンの音をリアルタイムで検知し、ユーザーへ通知するシステムです。 
主に以下のようなシナリオでの活用を想定しています：

- インターホンが鳴っても気づかない状況の補助
- 離れた場所からの通知（LINEなど）
- 障害者・高齢者支援（視覚的通知など）

### 注意点


### 開発環境

- Raspberry Pi 3B+
- Bluetoothヘッドセット（音声入力）

### 想定される通知手段

- LINE通知（Messaging API）
- パトランプ点灯（GPIO制御）

---

## パッケージのインストール

`sudo apt install python3 python3-pip python3-venv python3-numpy libsndfile1 ffmpeg hub-ctrl`  
`pip install sounddevice`

## 音声の準備

referenceフォルダを作成  
reference直下のinterphone.wavに、実際に検出したいインターホン音を録音して保存

# NOTICE

## 概要

`NOTICE` は、Bluetoothマイクと Raspberry Pi を用いてインターホンの音をリアルタイムで検知し、ユーザーへ通知するシステムです。  
主に以下のようなシナリオでの活用を想定しています：

- インターホンが鳴っても気づかない状況の補助
- 離れた場所からの通知（LINEなど）
- 障害者・高齢者支援（視覚的通知など）

### 注意点

本システムではhub-ctrlを使用して、USBハブの電源を物理的にオン/オフしています。
Raspberry Pi 3B+ では個別のUSBポート制御ができず、全ポートがまとめてオフになります。
そのため、USB接続のマウスやキーボードも一時的に使えなくなります。
通常は SSH接続して動作させる運用を想定しています。

### 開発環境

- Raspberry Pi 3B+
- Bluetoothヘッドセット（音声取得）

### 通知手段

- LINE通知（Messaging API）
- パトランプ点灯（USB制御）

---

## パッケージのインストール

`sudo apt install python3 python3-pip python3-venv hub-ctrl`  
`pip install sounddevice scipy numpy python_speech_features scikit-learn python-dotenv`

## 音声の準備

referenceフォルダを作成  
reference直下のinterphone.wavに、実際に検出したいインターホン音を録音して保存

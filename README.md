# NOTICE

## 概要

Raspberry Piで動作する、インターホン音検知＆通知システムです。  
Bluetoothマイクで音をリアルタイムに録音し、MFCCによる特徴抽出と類似度判定を用いて、特定のインターホン音を検出します。  
検出時には LINE への通知および USB 接続のパトランプを点灯させることで、離れた場所でも気づけるように設計されています。  
検知の開始・停止・状態確認は、LINE メッセージを通じて遠隔操作が可能です。  

### 想定利用シーン

- インターホンが鳴っても気づかない状況の補助
- 外出先や別の部屋からの通知受信（LINE 経由）
- 高齢者や聴覚障害のある方への支援（視覚通知）

### 注意点

本システムでは `hub-ctrl` を使用して USB ハブの電源を制御しています。  
Raspberry Pi 3B+ では USB ポート単位の制御ができず、全ポートが一括で ON/OFF されます。  
このため、一時的に USB マウスやキーボードも使用不可となる点にご注意ください。

通常は SSH 経由で操作する運用を想定しています。

### 開発環境

- Raspberry Pi 3B+
- Bluetoothヘッドセット（音声取得）
- Python 3.11

### 通知手段

- LINE通知（Messaging API）
- パトランプ点灯（USB制御）

### 使用方法

LINE developersのコンソールにあるwebhook URLに、自サーバーのURLを設定しておく必要があります。  
本プロダクトではngrokを使用してパブリックURLを生成し、公開しています。  

まず `webhook_server.py` を起動しておきます。  
LINE の公式アカウントに対して以下のメッセージを送信することで検知を操作できます：

- `開始` → 検知を開始します
- `停止` → 検知を停止します
- `状態` → 現在の検知状況を返信します

---

## セットアップ

### パッケージのインストール

```bash
sudo apt install python3 python3-pip python3-venv hub-ctrl  
pip install sounddevice scipy numpy python_speech_features scikit-learn python-dotenv flask psutil requests
```

### 環境変数

```bash
cp .env.sample .env  
LINE_ACCESS_TOKEN=（あなたのチャネルアクセストークン）  
LINE_USER_ID=（通知を受け取るLINEユーザーのID）
```

### 音声の準備

referenceフォルダを作成し、検出対象のインターホン音を録音してinterphone.wav として保存します。

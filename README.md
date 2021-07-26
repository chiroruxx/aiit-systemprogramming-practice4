# aiit-systemprogramming-practice4

# Abstruct
[esa.io](https://esa.io)から本日投稿された記事を取得し、Slackに通知するスクリプトです。

# Requirements
以下が必要ですので、事前に準備してください。
- esa.io のアクセストークン
- Slackの Incoming Webhook

また、実行するためには Python3 が必要です。

# Installation
```sh
$ pip install python-dotenv
$ cp .env.example .env
```

`.env` 内の値を埋めてください。

# Usage
```sh
$ python new_post_notification.py
```

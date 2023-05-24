# t14re-capture-app
t14re-capture-appは，エスタカヤ電子工業株式会社[1]から提供されているミリ波レーダモジュール評価キット TITAN [2]の一種である T14RE シリーズを用いてデータを取得するための非公式のプロジェクトです。

デモ用のプログラムは評価キット購入時に提供されていますが，本プロジェクトはその利便性を高めるためのものです。

## t14re_captureApp
PCとレーダを接続しデータをキャプチャする、本プロジェクトのメインのアプリです。
![app_overview](https://github.com/kossyprg/t14re-capture-app/assets/60993969/55ccdec8-b797-4990-8f3f-83e5645e8808)

キャプチャ方法は以下の3通りです。
- 指定されたファイル数（Set max files）
- Stopボタンを押下するまで（Endless mode）
- 指定された時刻に開始・終了（Scheduled mode）

## t14re_bin2matConverter
t14re_captureApp で取得したバイナリのデータを、MATLABで使用できるmatファイルへ変換するアプリです。
![converter_overview](https://github.com/kossyprg/t14re-capture-app/assets/60993969/1cd509b3-69d1-4388-b748-fbfa7acaf04d)

# ソースコードについて
exeファイルは、リポジトリにあるpyファイルをpyinstallerで変換することによって得られます。

# 注意事項
以下を承知の上，ご利用ください．
- 利用には，評価キットおよび添付された動作設定ファイル（.cfg）が必要です．
- 本プロジェクトはエスタカヤ電子工業（株）と無関係です．本プロジェクトに関するエスタカヤ電子工業（株）への問い合わせは控えてください．
- 評価キットに添付されたマニュアルに従い，技適（技術基準適合証明）に反する使用方法はしないでください．
- 主に 100 fps の設定ファイルを用いて動作確認を行っています。他の設定ファイルでは正常に動作しない可能性があります。

# 参考サイト
[1] [エスタカヤ電子工業（株） レーダーモジュール](https://www.s-takaya.co.jp/product/radar/)

[2] [丸文（株） ミリ波レーダモジュール評価キット TITANのご紹介](https://www.marubun.co.jp/technicalsquare/9141/)

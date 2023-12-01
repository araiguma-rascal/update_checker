# 概要
論文サイト(APL)の変更を検知し、LINE Notifyで通知してくれます。

# 目次
- Setup
    - ローカルでのテスト
    - LINE Notifyの設定
    - Githubの設定

## ローカルでのテスト
1. アプリを編集したいディレクトリでgit cloneを実行します。
```
git clone <このディレクトリのgit URL>
```
2. `.sample.env`ファイルの名前を`.env`に変更し、環境変数を書き換えます。この環境変数は下に記載する「LINE Notifyの設定」から取得してください。この`.env`ファイルはローカルでのテストでのみ有効です。Github Actionsで実行するためには、後述の「Githubの設定」を参考にしてください。この`MAIL`, `PASSWORD`は、APLのメールアドレスとパスワードです。
```
LINE_NOTIFY_TOKEN=<YOUR_LINE_NOTIFY_TOKEN>
MAIL=<YOUR_MAIL>
PASSWORD=<YOUR_PASSWORD>
```
3. pythonファイルを実行します。これによって、(最初の実行と、以降変更があった時に)LINEに通知が飛びます。
```
python update_checker.py
```

## Githubの設定
1. Cloneしたgit repositoryを、自分のリポジトリとしてGithub上に作成する。
2. Settings → Secrets and variables → Actions → Repository secretsに環境変数`LINE_NOTIFY_TOKEN`, `MAIL`, `PASSWORD`を入力する。
3. 6時間に一回Github Actionsによって定期実行される。
4. このプログラムは、変更がある度に新しい`status.txt`をpushしなければなりません。新しい`status.txt`は自分のrepositoryのActionsタブから、実行されたworkflowをクリックすればダウンロードできます。それをpushしてください。
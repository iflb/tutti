# インストール

### 1. Dockerの準備

Tuttiの作業環境を構築するには、最初にホストサーバーに**Docker**と**Docker Compose**をインストールする必要があります。 \
インストール手順は実行環境によって異なる場合があるため、最新の公式インストール手順に従ってください。

- [Install Docker](https://docs.docker.com/get-docker/)
- [Install Docker Compose](https://docs.docker.com/compose/install/)

### 2. TuttiリポジトリをCloneする

```bash
git clone https://github.com/iflb/tutti
```

### 3. Tuttiのアクティベート

#### [任意] Let'sEncryptを使用したSSLの自動設定

すでにWebドメイン名を取得済みの場合、Tuttiサービスを開始するたびに[Let's Encrypt](https://letsencrypt.org)を介してSSL認証を自動的に要求/更新することで、すべてのWebページを`https://`経由で提供することが可能です。これは、[Amazon Mechanical Turk](https://mturk.com)などのクラウドソーシングプラットフォームの使用を計画している場合に特に必要です。

この機能を有効にするには、最初に環境構成ファイル`tutti/.env`を次のように編集する必要があります。

**tutti/.env**
```diff

- DOMAIN_NAME=localhost
- EMAIL=
+ DOMAIN_NAME=yourdomain.com
+ EMAIL=my.email.address@for.letsencrypt.contact.info.com
...
- ENABLE_SSL=0
+ ENABLE_SSL=1
...
```

?> また、ホストサーバーのポート番号80と443を開くように設定する必要があることにも注意してください。

#### ビルド

以下のコマンドを実行します（これには少なくとも数分かかる場合があります）。

```bash
sudo docker-compose build
```

#### 起動

以下のコマンドを実行します（これにはさらに数分かかる場合があります）。

```bash
sudo docker-compose up
```

次に、以下に示すようなメッセージが表示されるまで待ちます（これは、Vue CLIがフロントエンドサーバーを正常に起動したことを意味します）。

<img src="./_media/vue-ready-output.png" />

### 4. Tuttiコンソールの確認

Webブラウザ（Google Chromeを推奨）を介して`https://yourdomain.com/vue/console/`（SSLを使用したWebホスティングの場合）または`http://localhost/vue/console/`（ローカルホストの場合）にアクセスします。コンソールに「Websocket connected」という緑色の表示があることを確認します。これは、DUCTSバックエンドサーバーが正常に起動されたことを意味します。

<img src="./_media/console-ready-screenshot.png" width="700" />

**準備はこれで完了です！** Tuttiを使ってアノテーションプロジェクトの開発を始めていきましょう。

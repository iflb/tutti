# プロジェクト・テンプレートの作成

## プロジェクト

Tuttiにおける**プロジェクト**とは、研究題目、アンケートのタイトル、あるいはHuman-In-The-Loop AIシステムに割り当てたいTuttiの役割などに対応します。例えば：

- 人間の顔画像のラベリングタスク
- COVID-19のソーシャルディスタンスに関する調査
- 会話型ロボットのWizard-of-OZエンジン

さあ、最初のプロジェクトを作ってみましょう！

### 手順

1. 上部のナビゲーションバーのアイコン<svg width="24" height="24" viewBox="0 0 24 24"><path d="M12,16A2,2 0 0,1 14,18A2,2 0 0,1 12,20A2,2 0 0,1 10,18A2,2 0 0,1 12,16M12,10A2,2 0 0,1 14,12A2,2 0 0,1 12,14A2,2 0 0,1 10,12A2,2 0 0,1 12,10M12,4A2,2 0 0,1 14,6A2,2 0 0,1 12,8A2,2 0 0,1 10,6A2,2 0 0,1 12,4Z" /></svg>をクリックし、[Create New Project...]を選択します。
2. プロジェクト名を`first-project`とし、"CREATE"をクリックします。
   <img src="./_media/create-prj-screenshot.png" />

3. ナビゲーションバーのプロジェクト一覧から、作成した`first-project`を選択します。

## テンプレート

**テンプレート**とは、プロジェクトにおいてユーザー（アノテーターなど）に提示される、静的にレンダリングされるウェブページコンポーネントです。COVID-19のソーシャルディスタンスに関する調査を例にとると、考えられるテンプレート（Webページ）群は次のようになります。

- *事前設問*において、参加者の年齢、性別、居住国などを質問する。
- *メイン設問*において、参加者の症状、最近行った場所などに関して質問する。
- *事後設問*において、本調査を終えた参加者としての意見・感想を聞く。

それでは、`first-project`上でいくつかテンプレートを作ってみましょう！

### 手順　

以降、本チュートリアルでは、`first-project`が単純な*画像ラベリングタスク*を想定し、それに付随する小さな事前調査と事後調査があると仮定します。

1. 左側のメニューの「Templates」に移動します。
2. 右側のウィンドウで、<svg width="24" height="24" viewBox="0 0 24 24"><path d="M18 11H15V14H13V11H10V9H13V6H15V9H18M20 4V16H8V4H20M20 2H8C6.9 2 6 2.9 6 4V16C6 17.11 6.9 18 8 18H20C21.11 18 22 17.11 22 16V4C22 2.9 21.11 2 20 2M4 6H2V20C2 21.11 2.9 22 4 22H18V20H4V6Z" /></svg>アイコンをクリックします。
3. テンプレート名に`prelimianry`と入力し、テンプレートプリセットに`Vuetify - Survey`を選択します。
4. 次のようなテンプレート名とテンプレートプリセット名で、2.と3.をあと3回繰り返します。
  - main1、 Vuetify - ImageLabeling
  - main2、 Vuetify - SimpleSurvey
  - post、 Vuetify - SimpleSurvey
5. `preliminary`、`main1`、`main2`、および`post`と命名された合計４つのテンプレートがドロップダウンメニューに表示されていることを確認します。

    !> 作成されたテンプレートはすぐには反映されない場合があります。強制リロードするには、ターミナルでCtrl-Cを押してDockerアプリケーションを停止し、再度実行します。

6. プルダウンメニューで各テンプレートを選択して、ページが正しく表示されることを確認します。表示されたテンプレートでは、ユーザー入力がメモリに記録される様子や、送信時に結果がどのように表示されるかをテストすることもできます。
   <img src="./_media/template-demo.gif" width="600" />

7. `main2`のテンプレートファイルを開き、次のように行を編集します**（これを行う方法については、すぐ下の「テンプレートの編集」に記載されています）**。
    ```
    <<<<< (編集前)
    <header><b>Q.</b> Copy-and-paste your Worker ID.</header>
    =====
    <header><b>Q.</b> Describe what you saw in the right picture.</header>
    >>>>> (編集後)

    <<<<<
    <v-text-field outlined flat v-nano.required v-model="workerId" label="Worker ID" />
    =====
    <v-text-field outlined flat v-nano.required v-model="description" label="Describe..." />
    >>>>>

    <<<<<
    data: () => ({ workerId: "" })
    =====
    data: () => ({ description: "" })
    >>>>>
    ```


### テンプレートの編集

上記の手順7で説明したように、このチュートリアルでは`main2`に少し変更が必要です。ファイルを編集してみましょう。同時に、他のファイルも後でスムーズに編集できるように、いくつかの重要なポイントもお伝えしたいと思います。

#### ファイルの場所

`first-project`プロジェクトの`main2`テンプレートは`tutti/projects/first-project/templates/main2/Main.vue`にあります。より汎用的には、
```
tutti/projects/<project-name>/templates/<template-name>/Main.vue
```
が、あるプロジェクトのあるテンプレートのファイルパスとなります。


#### .vueファイル形式
テンプレートのファイル形式には.vue拡張子が付いており、これは[Vue.js](https://vuejs.org/)の[単一ファイルコンポーネント](https://vuejs.org/v2/guide/single-file-components.html)を意味します。
簡単に言えば、HTML、CSS、JavaScriptを一つのファイルにまとめて記述可能なファイルであり、他のWebページコンポーネントに意図しない影響を与えないように適切なスコープを設定することが出来ます。詳細については、[公式ドキュメント](https://vuejs.org/v2/guide/single-file-components.html)を参照してください。

#### 基本的なコーディング例

たとえば、`main2`テンプレートの`Main.vue`は次のようになります（このテンプレートは、マテリアルデザイン用のVue UIライブラリである[Vuetify](https://vuetifyjs.com/en/)を使用していることに注意してください）。

```main2/Main.vue

<!-- Your HTML code here -->
<template>   
    <v-container pa-10>
        <v-card width="600" class="mx-auto my-6 pa-6">
            <v-row>
                <v-col cols="12">
                    <header><b>Q.</b> Describe what you saw in the right picture.</header>
                </v-col>
                <v-col cols="12">
                    <v-text-field outlined flat v-nano.required v-model="description" label="Describe..." />
                </v-col>
            </v-row>
            <v-row class="d-flex" justify="end">
                <v-btn class="mr-3 mb-3" :disabled="!canSubmit" @click="canSubmit ? submit() : false">next</v-btn>
            </v-row>
        </v-card>
    </v-container>
</template>

<!-- Your JavaScript code here -->
<script>   
import nanoMixIn from "@/mixins/nano";
export default {
    mixins: [nanoMixIn],
    data: () => ({ workerId: "" })
};
</script>

<!-- Your CSS here -->
<style scoped>   
</style>
```

Vue.jsとVuetifyのプログラミング作法に加えて、Tutti独自のプログラミングルールがいくつかあります（JavaScriptの関数や[Vueカスタムディレクティブ](https://vuejs.org/v2/guide/custom-directive.html)など）。具体的には、

- `v-nano`：このVueディレクティブが入力タグ/コンポーネントに追加されると、`v-model`に指定されたキーとその値が、タスク完了時にTuttiサーバーへ送信されるユーザー入力情報として登録されます。さらに`.required`が追加された場合、そのキーは必須項目として扱われます（`canSubmit`を参照）。
- `submit()`：この関数が呼び出されると、`v-nano`が付与されているすべてのユーザー入力がTuttiサーバーに送信され、次のテンプレートがロードされます。
- `canSubmit`：`v-nano.required`として登録されているすべての項目に有効な入力値があるかどうかを示す、バイナリのcomputedプロパティ。これは、条件を満たすまで送信ボタンをクリック不可にするなどの目的で用いることができます。
- `nanoMixIn`：Tuttiプロジェクトのテンプレートで使用される重要なデータ、メソッド、およびフックを含むVueミックスインモジュールです。これは常にファイル内でロードする必要があります。
詳細およびその他のプログラミング規則については、[プログラミングリファレンス>テンプレート](/guide/ref_template)を参照してください。

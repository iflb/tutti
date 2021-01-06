# ナノタスクのアップロード

これで、作成したテンプレートとフローがアノテーションプロジェクトを構築するためにどのように連携するかが分かったかと思います。
*でも*、少し変だと思いませんでしたか？次のようなことを思ったかもしれません：
- 同じ画像のペアを何度もアノテーションさせる意味はあるのか？（実際のアノテーションタスクのためには、何千個もテンプレートを作らないといけないのか？）
- ~~右側のカードに何が表示されていたか、毎回ワーカーに質問するのは冗長ではないか？必要なときだけそれを聞くようにできないか？~~<span style="color:red">近日中対応予定</span>

もっともな質問だと思います！大丈夫です、ちゃんと答えはあります。

## ナノタスク

**ナノタスク**とは、同じテンプレートを使用してレンダリングされるタスクのインスタンスを指します。これらはすべて同じパラメーター集合を共有し、それぞれが異なる値を持つことができます。
たとえば、画像ラベリングの`main1`テンプレートは、ある決まった画像ペアの比較のみを目的としているわけではありません。むしろ、これは文字通り単なる**テンプレート**にしかすぎません。
このテンプレートに動的にレンダリングされる実際のコンテンツはナノタスクによって所有され、ワーカーがフローに従ってテンプレートのノードに入るタイミングで、一つのナノタスクがロードされます。

`main1`の`Main.vue`を見てみましょう。コードのHTML部分では、画像のソースURL（`<v-img>`の:src属性）はオブジェクト変数のようなもの（例：`nano.data.img_url0`）が、入っていて、固定値のURLではないことがわかります。

```main1/Main.vue

<template>
    <v-container pa-10>
        <div class="text-h4">Main-1</div>

        <v-card max-width="1000" class="mx-auto my-6 pa-6">
            <v-row align="center">
                <v-col cols="5">
                    <v-card class="pa-3" color="grey lighten-4">
                    <v-img height="300" :src="nano.data.img_url0" contain>

                        <template v-slot:placeholder>
                            <v-row class="fill-height ma-0" align="center" justify="center">
                                <v-progress-circular indeterminate color="grey lighten-1"></v-progress-circular>
                            </v-row>
                        </template>

                    </v-img>
                   </v-card>
                </v-col>
                <v-col cols="2" align="center" justify="center"><v-icon x-large>mdi-arrow-left-right-bold</v-icon></v-col>
                <v-col cols="5">
                    <v-card class="pa-3" color="grey lighten-4">
                    <v-img height="300" :src="nano.data.img_url1" contain>
                        <template v-slot:placeholder>
                            <v-row class="fill-height ma-0" align="center" justify="center">
                                <v-progress-circular indeterminate color="grey lighten-1"></v-progress-circular>
                            </v-row>
                        </template>
                    </v-img>
                    </v-card>
                </v-col>
            </v-row>
            <v-row class="d-flex" justify="center">
                <v-btn class="ma-3" x-large dark color="green darken-4" @click="nano.ans.choice='Same';  submit()">Same</v-btn>
                <v-btn class="ma-3" x-large dark color="green darken-1" @click="nano.ans.choice='Maybe Same';  submit()">Maybe Same</v-btn>
                <v-btn class="ma-3" x-large dark color="red darken-1"   @click="nano.ans.choice='Maybe Not Same';  submit()">Maybe Not Same</v-btn>
                <v-btn class="ma-3" x-large dark color="red darken-4"   @click="nano.ans.choice='Not Same';  submit()">Not Same</v-btn>
            </v-row>
        </v-card>
    </v-container>
</template>

<script>
import nanoMixIn from "@/mixins/nano";
export default {
    mixins: [nanoMixIn],
    data: () => ({
        defaultNanoProps: {
            "img_url0": "https://images-na.ssl-images-amazon.com/images/I/61qEl7SAq9L._AC_SL1000_.jpg",
            "img_url1": "https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcQJxhbQz2Oy8Dn8ksxkaXPbzMIvhTaGUBH98P5nQ9zIXlQVV5OnWT1ozp9joA&usqp=CAc"
        }
    })
};
</script>
```

厳密に言えば、属性キーにコロンの接頭辞がある場合（例えばここでは`:src`を指す）、文字列値`nano.data.img_url0`と`nano.data.img_url1`という値はJavaScriptオブジェクト変数として解釈されます。
これは、Vue.jsの構文の一つです。これは、変数の値によってHTML属性の値を指定する[`v-bind`ディレクティブの省略形](https://vuejs.org/v2/guide/syntax.html#v-bind-Shorthand)です。 
`nano.data`はTutti用に予約された構造であり、`img_url0`および`img_url1`というキーの値はあるナノタスク情報から読み込まれ、`src`属性の値として補間されます。
Tuttiでは、これらのナノタスクが持つフィールド群を**nano-props**と呼びます。

#### デフォルト値

では、テスト実行の時に見たかわいいクマの画像はどこから来たのでしょうか？
これらはプレースホルダー値として、JavaScriptコード内に`defaultNanoProps`のメンバーとして定義されています。
プレースホルダー値は、ナノタスクがテンプレートにまだ登録されていない場合、またはブラウザーコンソールの[Template]ページでテンプレートをテストする場合に使用されるものです。
アノテーションシステムとしての実際の使用時には、プロジェクトを実行する前にナノタスクを登録して、画像の組が動的にロードされるようにする必要があります。

!> `defaultProps`は、Tutti用に予約されているVueの`data`オブジェクトのキーの一つとして`nanoMixIn`モジュールに定義されています。

以下では、`main1`テンプレートへナノタスクデータをアップロードする方法について説明します。

### 手順

1. ブラウザコンソールのサイドバーメニューから、[Task Flow]ページに移動します。

2. `main1`テンプレートのカードの<svg width="24" height="24" viewBox="0 0 24 24"><path d="M12,16A2,2 0 0,1 14,18A2,2 0 0,1 12,20A2,2 0 0,1 10,18A2,2 0 0,1 12,16M12,10A2,2 0 0,1 14,12A2,2 0 0,1 12,14A2,2 0 0,1 10,12A2,2 0 0,1 12,10M12,4A2,2 0 0,1 14,6A2,2 0 0,1 12,8A2,2 0 0,1 10,6A2,2 0 0,1 12,4Z" /></svg>アイコンをクリックして、「Import Nanotasks ...」を選択します。

3. `tutti/projects/first-project/templates/main1/`にある`sample-nanotasks.json`を選択します。~~プレビューでは、インポートする各ナノタスク（行として表される）の画像URLのリストが表示されます。 ~~次に、「IMPORT」をクリックします。

4. 「Nanotasks（15）」というボタンが表示されていれば、ナノタスクが正常にインポートされたことを意味します。そのボタンをクリックすると、インポートされたナノタスクのリストが表示されます。

  <img src="./_media/imported-nanotasks.png" width="500" />

5. Tuttiサービスを再起動し（またはTuttiのバックエンドサービスを`docker-compose restart backend`で再起動し）、ブラウザコンソールを更新します。

6. もう一度「Launch in Production Mode (Private)」に移動し、アノテーションタスクを開始します。`main1`テンプレートの画像は、登録されたナノタスクで使用されているURLのものとなっているでしょう。

### ナノタスク用JSONの理解

現在、nanotasksをアップロードするために準備されている唯一の方法は、JSONファイルを使用することです。 
`sample-nanotasks.json`には次の形式の情報が含まれています。

```json
{
    "Settings": {
        "TagName": "mytagname",
        "NumAssignable": 3,
        "Priority": 1
    },
    "Nanotasks": [
        {
            "NumAssignable": 2,      // <--- グローバル値(3)を上書き
            "Priority": 3,           // <--- グローバル値(1)を上書き
            "Props": {
                "img_url0": "/static/trump-left.jpg",
                "img_url1": "/static/trump-right-1.jpg"
            },
            "GroundTruths": {
                "choice": "Same"
            }
        },
        ...
    ]
}
```

「Settings」という名前の最上位メンバーは、ファイルで定義されているすべてのナノタスクに適用されるグローバル設定のパラメーターを指定します。

`TagName`はナノタスクのユーザ定義グループを作成するために有用です：ナノタスクを操作するイベント（例えば`UploadNanotasks`や`DeleteNanotasks`）において、この定義グループをクエリに指定することができます。任意の文字列の指定が可能ですが、アップロードされたすべてのナノタスクをより簡単に追跡できるように、以前にアップロードされた他のナノタスクグループの文字列とは異なるものにすることをお勧めします。

`NumAssignable`は、ナノタスクに割り当てたいワーカーの数を指します。
`Priority`は、ナノタスクの割り当て順序をソートする基準となる整数値です。数字が小さいほど、より重要なナノタスクとして扱われます。
`Settings`の子要素キーとして指定された`NumAssignable`と`Priority`は、ファイルに記述されているすべてのナノタスクに適用されます; `Nanotasks`リスト内の子要素のメンバーとして個別に設定されているナノタスクにおいては、グローバル値は上書きされます。

`Props`は、ナノタスクが1つずつ読み込まれるときにテンプレートに動的にレンダリングするコンテンツで、key-valueデータです。
各キーはテンプレートに表示されるものに対応している必要があり、その値は文字列として指定が可能です。

`GroundTruths`もまたkey-valueデータであり、`FlowNode`の条件ステートメント（[プロジェクトスキーム](guide/ref_scheme.md)を参照）でワーカーの回答を答え合わせするための、またはワーカーの回答が収集された後に用いるための正解データです。

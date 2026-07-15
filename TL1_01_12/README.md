# TL1_01_12 ローダーと配置

Blender版レベルエディタが出力したJSONをC++ゲーム側で読み込み、モデルを配置する機能です。

## 実装した内容

- `nlohmann/json`によるJSON解析
- ルート、`name == "scene"`、`objects`配列の検証
- `type`、`name`、`file_name`、Transform、Colliderの読み込み
- `children`の再帰読み込み
- Blender座標系からゲーム座標系への変換
- 回転の度数法からラジアンへの変換
- `file_name`を使ったモデル取得・読み込み
- `Object3d`の生成と位置・回転・スケールの設定
- ゲーム内ファイルメニューからのJSON選択
- 日本語を含むWindowsパスへの対応
- 読み込み確認中にレール進行を停止するプレビューモード

## 動作確認

Debug x64でビルドし、警告0・エラー0を確認しました。

ゲーム内で次の操作を行っています。

1. `F1`でGUIを表示
2. `ファイル`から読み込みを選択
3. `resources/blender_level_sample.json`を選択
4. SuzanneとBunnyの2モデルが配置されることを確認
5. Colliderデータ1件が読み込まれることを確認

確認結果は [evidence/load_result.png](evidence/load_result.png) にあります。

## ファイル構成

`project`以下は、実際のCG2プロジェクトで追加・変更したファイルを元のパスのまま収録しています。このフォルダだけでは単独ビルドできないため、完全な実行プロジェクトは下記のCG2リポジトリを参照してください。

- 実装ブランチ: <https://github.com/KOIKOIMARU/CG2/tree/TL1%E8%AA%B2%E9%A1%8C%E7%94%A8>
- 動作確認済みコミット: <https://github.com/KOIKOIMARU/CG2/commit/44bf27ad8ec04a3ef23903e3e3ca443d8abbbd52>

## 現在の実装範囲

- 子オブジェクトは再帰的に読み込みます。現在の`Object3d`に親Transform機能がないため、ゲーム上では個別のオブジェクトとして配置します。
- Colliderの`type`、`center`、`size`は読み込んで保持します。既存ゲームの衝突判定への接続は行っていません。
- 動的モデル読み込みはOBJ、glTF、GLBに対応しています。

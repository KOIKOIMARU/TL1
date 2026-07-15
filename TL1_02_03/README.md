# TL1_02_03 無効フラグ

Blender上のオブジェクトに`disabled`フラグを設定し、ゲームへの配置を有効・無効にできる機能です。

## 実装した内容

- オブジェクトへbool型の`disabled`カスタムプロパティを追加するオペレーター
- オブジェクトプロパティに`Disabled`パネルを追加
- 未設定時は`Add Disabled`ボタン、設定後はチェックボックスを表示
- BlenderのJSON出力へ`disabled`を追加
- C++ローダーで`disabled`をbool値として読み込み
- `disabled`が`true`のオブジェクトはゲームへ配置しない
- `disabled`が未設定または`false`のオブジェクトは従来どおり配置
- 無効な親オブジェクトの子も配置しない

## 動作確認

- Blender 4.4.1のバックグラウンド実行で、アドオンの登録・無効フラグ追加・JSON出力・登録解除を確認
- CG2をDebug x64でビルドし、警告0・エラー0を確認

ゲーム側の確認用JSONには、通常配置されるSuzanneとBunnyに加えて、`disabled: true`の`DisabledSuzanne`を収録しています。ゲームで読み込むと、配置数は2になり、`DisabledSuzanne`は表示されません。

## ファイル構成

- Blenderアドオン本体: リポジトリ直下の`level_editor`フォルダ
- ゲーム側の変更ファイル: `TL1_02_03/project`以下

`project`以下は、実際のCG2プロジェクトで変更したファイルを元のパスのまま収録しています。このフォルダだけでは単独ビルドできないため、完全な実行プロジェクトは下記のCG2リポジトリを参照してください。

- 実装ブランチ: <https://github.com/KOIKOIMARU/CG2/tree/TL1%E8%AA%B2%E9%A1%8C%E7%94%A8>
- 動作確認済みコミット: <https://github.com/KOIKOIMARU/CG2/commit/7e08cb79b66cab503b3f797d3fc522ae50aaaad7>

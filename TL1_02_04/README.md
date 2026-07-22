# TL1_02_04 自キャラSpawnPoint

Blender上で自キャラの出現位置を配置し、JSONを介してCG2のプレイヤーへ反映する機能です。

## 実装した内容

- `spawn.py`にSpawnPointモデルの読込オペレーターと配置オペレーターを追加
- 初回だけOBJを読み込み、2個目以降は同じメッシュデータを共有して複製
- 読込元の`PrototypePlayerSpawn`はシーンから外し、JSONへ混入しないように管理
- `MyMenu`から「出現ポイントシンボルの作成」を実行可能
- SpawnPointへ`type = "PlayerSpawn"`カスタムプロパティを設定
- JSON出力時、`type`カスタムプロパティがあればBlender標準タイプより優先
- C++側に`PlayerSpawnData`と`players`配列を追加
- `PlayerSpawn`を再帰的に検索し、無効化されていない座標・回転を読み込み
- 最初のSpawnPointをプレイヤーの位置・回転・レール距離へ反映
- SpawnPointがないJSONでは従来の初期位置を維持

## 動作確認

- Blender 4.4.1のバックグラウンド実行で、アドオン登録、SpawnPointの2個配置、モデル共有、JSON出力、登録解除を確認
- JSONに`type: "PlayerSpawn"`が2件出力されることを確認
- CG2をDebug x64でビルドし、警告0・エラー0を確認

## ファイル構成

- Blenderアドオン本体: リポジトリ直下の`level_editor`フォルダ
- ゲーム側の変更ファイル: `TL1_02_04/project`以下

`project`以下は、実際のCG2プロジェクトで変更したファイルを元のパスのまま収録しています。このフォルダだけでは単独ビルドできないため、完全な実行プロジェクトは下記のCG2リポジトリを参照してください。

- 実装ブランチ: <https://github.com/KOIKOIMARU/CG2/tree/TL1%E8%AA%B2%E9%A1%8C%E7%94%A8>


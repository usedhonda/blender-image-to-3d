# Blender Image to 3D

`blender-image-to-3d` は、承認済みの参考画像から編集可能な Blender シーンを作ります。呼び出し例:

```text
$blender-image-to-3d /path/to/image
```

既定の成果物は、元画像の画風、比率、見えている非対称性、同一性に重要な特徴を保った静止・編集可能 `.blend` です。観測できた事実、推測した部分、未決定の部分を分けて記録します。Blenderでの直接構築、素体の調整、image-to-3D、混成経路を用途に応じて選びます。

## 承認ゲート

制作開始前に、範囲、同一性の核、比率、部品、接合、材質、表情、推測部分を含む完全なデザイン案を人間が承認します。ブロックアウトと代表材質を作った後、仕上げへ進む前に、粗い形と材質をもう一度人間が確認します。デザイン承認後、既に許可された外部サービスで粗い候補を作ることはできます。新しいサービスへの送信や費用は個別に確認します。

設計・レビューには、明示的なホスト設定で利用できる場合 GPT-6 Astra の高推論を優先し、制作は GPT-6 Astra の低推論・fork なしへ渡します。これはホスト側の選択であり、このskillが実行中のモデルを自動変更することはありません。手動切替が必要なら、設定済みモデルとホストを先に確認します。MCPは必須ではありません。公式 Blender MCP の参照先は <https://projects.blender.org/lab/blender_mcp> です。

## 消費を抑える制作手順

CLI・MCPのどちらでも関連操作をまとめ、Astra HighからLowへ承認済みの制作契約だけを渡します。修正は影響する部品・視点に限定し、条件が変わらない合格証拠を再利用します。待機はホスト側で処理し、情報が増えないモデル呼出しを避けます。承認と最終の書出し検証は維持します。

取得できる使用量を設計・引継ぎ・制作・修正・検証まで合算し、APIトークン・料金とCodex利用枠を分けます。High→Lowの節約効果は未実測です。[消費の詳細資料](skills/blender-image-to-3d/references/token-efficiency.md)は診断・比較時だけ読み込みます。

## 成果物

- 意味のあるオブジェクト名とチェックポイントを持つ編集可能な `.blend`;
- 書き出し後の再読込と再レンダーを確認した交換形式（既定はGLB）;
- 元画像との比較、顔アップ、斜め、側面・背面、必要に応じて上面・下面の確認画像;
- 仮定、外部ジョブ、材質判断、既知の制限、未検証事項の記録。

表情、アニメーション、VRM・ゲーム向け納品、3Dプリントには追加の合格条件があります。生成画像、受付済みジョブ、見栄えのよいレンダーだけでは完成扱いにせず、メッシュを読み込み、検査し、保存し、再レンダーします。

## インストール

通常のローカルskillとして使う場合は、チェックアウト内のネストしたskillディレクトリだけをインストールします。先に既存パスを確認し、既存skillを上書きしません。

```bash
git clone https://github.com/usedhonda/blender-image-to-3d.git
mkdir -p ~/.codex/skills
if [ -e ~/.codex/skills/blender-image-to-3d ] || [ -L ~/.codex/skills/blender-image-to-3d ]; then
  echo "Existing installation preserved; inspect before updating."
else
  cp -R ./blender-image-to-3d/skills/blender-image-to-3d ~/.codex/skills/blender-image-to-3d
fi
```

`~/.agents/skills` を使うホストでは、同じ確認付きコピーを保存先だけ変えて行います。既に同名パスがある場合は内容を確認して保持し、必要なファイルだけを統合してください。リポジトリ直下の `.codex-plugin/plugin.json` は配布用マニフェストです。設定済みmarketplaceまたは対応するGUIインポートで利用できますが、このリポジトリは直接のプラグインインストーラーコマンドを保証していません。Blender本体と、任意の公式MCPサーバーは別の依存関係です。

## ファイル構成

- `skills/blender-image-to-3d/SKILL.md`: 呼び出し、承認ゲート、工程、完了条件。
- `skills/blender-image-to-3d/references/`: 経路選択、診断、外部ジョブ状態、ランタイム、書き出し検査。
- `skills/blender-image-to-3d/templates/`: brief、状態、Astra計画、handoff、品質記録、外部ジョブ記録。
- `skills/blender-image-to-3d/scripts/`: ランタイムが使える場合の承認付き状態管理とBlender操作。

設計に使った原マニュアルは調査資料であり、利用者が別途用意する必要はありません。

## 現在の検証状況

Blender 5.2.1環境で、Blenderを直接操作する経路と公式MCPが同じキューブレンダーを出力し、保存・再読込まで確認したことが基準検証です。R2では正面、背面、側面、斜め、上面、靴底、通常・笑顔、4種類の材質資料を作成しましたが、デザイン承認は保留中です。Astra Lowによるキャラクター制作実行はまだありません。証拠一覧と保留項目は [`docs/verification.md`](docs/verification.md) を参照してください。

## ライセンス

MITです。[`LICENSE`](LICENSE) を参照してください。

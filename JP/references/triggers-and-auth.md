# トリガーと接続・認証

| 種類 | 確認状況 | ヘルパー | `auth_mode` | 接続の `source` | コネクタのアクションの認証 |
|---|---|---|---|---|---|
| 手動でフローをトリガーする | 実機でインポートと実行を確認 | `manual_trigger` | `invoker` | `Invoker` | Raw 形式 (`X-MS-APIM-Tokens`) |
| 利用者が実行する SharePoint のトリガー (ファイルの選択時など) | 書き出し結果で確認 | なし | `invoker` | `Invoker` | Raw 形式 |
| スケジュール | トリガーのみ書き出し結果で確認 | `recurrence_trigger` | `embedded` | 未確認 (推論: `Embedded`) | 未確認 (推論: `$authentication`) |
| コネクタの自動実行 (例: ファイルが作成されたとき) | トリガーと `source` を書き出し結果で確認 | `polling_trigger` | `embedded` | `Embedded` | 未確認 (推論: `$authentication`) |

- 未確認の組み合わせを使う場合は、設計の要約で未確認として伝える。
- 利用者が実行する SharePoint のトリガーは、リージョン固有の `runtimeUrl` を含むため、ヘルパーを用意していない。使う場合は、そのトリガーを含むフローの `definition.json` を依頼者に求める。

## 手動トリガーの入力項目

`manual_trigger` の `properties` と `required` に JSON スキーマの形で渡す。

```python
manual_trigger(
    properties={"text": {"title": "JSON", "type": "string",
                         "x-ms-content-hint": "TEXT", "x-ms-dynamically-added": True}},
    required=["text"])
```

参照するときは `@triggerBody()?['text']`。

## スケジュール

- `startTime` は UTC で指定する。日本時間 10:00 は `01:00:00.000Z`。
- `interval` は書き出し結果では文字列 (`"1"`)。

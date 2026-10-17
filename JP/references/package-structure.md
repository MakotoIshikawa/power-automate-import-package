# パッケージの外枠 (確認済み)

`scripts/pa_package_builder.py` の `build_package` が作る。この内容は、ビルダーを修正する場合や、インポートが止まった場合の確認用。

```text
manifest.json
Microsoft.Flow/flows/manifest.json
Microsoft.Flow/flows/<GUID-A>/definition.json
Microsoft.Flow/flows/<GUID-A>/apisMap.json
Microsoft.Flow/flows/<GUID-A>/connectionsMap.json
```

- 最上位 `manifest.json` のフローのリソースのキー、`flowAssets.assetPaths`、フォルダー名は同じ GUID-A。
- `definition.json` の `name` と `id` の末尾は、GUID-A とは別の GUID-B。
- フローのリソースには `id` と `name` を持たせない。API のリソースには持たせる。
- `apisMap.json` と `connectionsMap.json` の値は、最上位 `manifest.json` の該当リソースのキー。
- `metadata` は作成者 ID などの書き出し元固有の値なので作らない。なくてもインポートできた。
- zip 内のフォルダーだけの項目は不要。
- 記憶だけで別の形式を組み立てた版は、インポート画面が「パッケージをインポートしています」のまま止まった。

# SharePoint

## 項目の作成 (`PostItem`、実機で確認済み)

| 列の種類 | パラメーター名 |
|---|---|
| サイト | `dataset` (サイト URL) |
| リスト | `table` (リスト ID の GUID。表示名ではない) |
| テキスト、複数行テキスト、数値、日付 | `item/<内部名>` |
| 選択肢 (単一) | `item/<内部名>/Value` |
| 参照列 (単一) | `item/<内部名>/Id` (参照先アイテムの SharePoint ID) |

- 参照列には参照先の ID を入れる。タイトルなどの文字列は入れない。
- 参照列の設定から追加した従属列は読み取り専用なので、値を設定しない。
- 作成結果の ID は `@outputs('<キー>')?['body/ID']`。
- null をテキスト列に渡すと空欄で登録される。
- 日付のみの列に `YYYY-MM-DD` を渡すと、画面では同じ日付で表示される。CSV では UTC で 1 日前に見えるため、CSV だけでずれと判断しない。
- ユーザー列、複数選択、複数値の参照など、上の表にない列の種類は、知識から作り、未検証として伝える。

## 書き出し結果で確認したアクション

`GetItem` (項目の取得)、`GetFileItem` (ファイル プロパティの取得)、`CreateFile` (ファイルの作成)、`GetOnNewFileItems` (ファイルが作成されたとき)。上記以外のアクションも知識から作ってよい。その場合は未検証として伝える。

## 列定義の確認方法

リスト ID や列の内部名が分からない場合は、依頼者にブラウザーで次の URL を開いてもらう。URL は末尾まで省略せずに示す。

リスト ID と表示名

```text
https://<テナント>.sharepoint.com/sites/<サイト>/_api/web/GetList('/sites/<サイト>/Lists/<リストの URL 名>')?$select=Id,Title
```

列の定義

```text
https://<テナント>.sharepoint.com/sites/<サイト>/_api/web/GetList('/sites/<サイト>/Lists/<リストの URL 名>')/fields?$filter=Hidden eq false and ReadOnlyField eq false&$select=Title,InternalName,TypeAsString,Required,Choices,LookupList,LookupField
```

参照列と従属列

```text
https://<テナント>.sharepoint.com/sites/<サイト>/_api/web/GetList('/sites/<サイト>/Lists/<リストの URL 名>')/fields?$filter=TypeAsString eq 'Lookup'&$select=Title,InternalName,IsDependentLookup,PrimaryFieldId,ReadOnlyField,Required
```

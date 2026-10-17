# Flow Design Standards

The goal is that someone other than the author can open the flow and understand both the processing and its intent.

## Action Names

**Keep the default action name and add the purpose after a separator.** The separator and the language of the action name are determined by the request language. Use the builder's `action_name(base, purpose, lang)`.

| Request language | Separator | Example |
|---|---|---|
| Japanese (`ja`) | Full-width colon `：` | `項目の作成：試験情報の登録` |
| English (`en`) | ` - ` (space, hyphen, space) | `Create item - Register study` |

Examples of default action names

| Japanese default name | English default name | Japanese example | English example |
|---|---|---|---|
| 作成 | Compose | 作成：ユーザー名 | Compose - User name |
| 変数を初期化する | Initialize variable | 変数を初期化する：検索条件 | Initialize variable - Search filter |
| 項目の取得 | Get item | 項目の取得：ユーザーデータ | Get item - User data |
| 項目の作成 | Create item | 項目の作成：試験情報の登録 | Create item - Register study |
| アレイのフィルター処理 | Filter array | アレイのフィルター処理：特定条件の抽出 | Filter array - Extract matching rows |
| JSON の解析 | Parse JSON | JSON の解析：子フローの応答 | Parse JSON - Child flow response |
| それぞれに適用する | Apply to each | それぞれに適用する：国別情報 | Apply to each - Country records |
| 条件 | Condition | 条件：承認済みか | Condition - Is approved |
| スコープ | Scope | スコープ：登録処理 | Scope - Registration |

- The English default names are based on knowledge. If they may differ from what the designer shows, report them as unconfirmed in the design summary.
- Half-width colons (`:`) can also be used in names, but this standard does not use them.
- In the key used in the definition, spaces are replaced with `_`. Example: the key for `Create item - Register study` is `Create_item_-_Register_study`. Use the key in expressions as well. Convert with the builder's `action_key()`.
- Do not rename triggers (`manual`, `Recurrence`, and so on).

## Notes

**Write the background, the meaning of conditions, the design reason, and cautions that the name alone cannot convey.** Notes are stored in the action's `description` (confirmed in an exported flow). Write notes in the request language.

Examples

- "Sets the ID of the created study record to the lookup column of the following country records."
- "The condition checks Status = Active."
- "Concurrency is set to 1 so that parent and child records stay matched."

Actions that must have notes

- Connector actions (get, create, update, send, and so on)
- Conditions, switches, loops, and scopes
- Parse JSON, Filter array, and Select

Compose and variable actions do not need notes if the name conveys the intent. Do not write notes that only restate the name.

## Structure

- **Scopes**: use when three or more related actions continue in a row and grouping makes the flow easier to follow. Do not put a few actions in a scope just to group them.
- **Conditions**: aim for at most two levels of nesting. If a value branches three or more ways, consider a switch.
- **Passing data**: use Compose for values that do not change. Use variables only when a value must be updated during the run.
- **Arrays**: use Select to reshape an array and Filter array to narrow it down. Do not create unnecessary loops.
- **Loops**: set concurrency to 1 when a later step uses an earlier result or when parent and child records must stay matched.

```json
"runtimeConfiguration": {"concurrency": {"repetitions": 1}}
```

## Do Not Over-apply

- Do not add processing, scopes, or variables that were not requested just to organize the flow.
- Do not turn a requirement to process multiple items into processing a single item with `first()` or similar.
- Prefer simplicity. Choose a readable sequence of actions over packing in complex expressions.

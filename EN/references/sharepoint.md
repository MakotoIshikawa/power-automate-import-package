# SharePoint

## Create Item (`PostItem`, confirmed by import and run)

| Column type | Parameter name |
|---|---|
| Site | `dataset` (site URL) |
| List | `table` (list ID GUID, not the display name) |
| Text, multiple lines of text, number, date | `item/<internal name>` |
| Choice (single) | `item/<internal name>/Value` |
| Lookup (single) | `item/<internal name>/Id` (SharePoint ID of the target item) |

- Set the ID of the target item in a lookup column. Do not set a string such as the title.
- Dependent lookup columns added from the lookup column settings are read-only. Do not set values for them.
- The ID of the created item is `@outputs('<key>')?['body/ID']`.
- Passing null to a text column leaves it blank.
- Passing `YYYY-MM-DD` to a date-only column shows the same date on screen. A CSV export may show the previous day in UTC, so do not judge a shift from the CSV alone.
- Column types not in the table above (person, multiple choice, multi-value lookup, and so on) may be written from knowledge; report them as unverified.

## Actions Confirmed in Exported Flows

`GetItem` (Get item), `GetFileItem` (Get file properties), `CreateFile` (Create file), `GetOnNewFileItems` (When a file is created). Other actions may also be written from knowledge; report them as unverified.

## Checking Column Definitions

If the list ID or column internal names are unknown, ask the requester to open the following URLs in a browser. Show each URL in full.

List ID and title

```text
https://<tenant>.sharepoint.com/sites/<site>/_api/web/GetList('/sites/<site>/Lists/<list-url-name>')?$select=Id,Title
```

Column definitions

```text
https://<tenant>.sharepoint.com/sites/<site>/_api/web/GetList('/sites/<site>/Lists/<list-url-name>')/fields?$filter=Hidden eq false and ReadOnlyField eq false&$select=Title,InternalName,TypeAsString,Required,Choices,LookupList,LookupField
```

Lookup and dependent lookup columns

```text
https://<tenant>.sharepoint.com/sites/<site>/_api/web/GetList('/sites/<site>/Lists/<list-url-name>')/fields?$filter=TypeAsString eq 'Lookup'&$select=Title,InternalName,IsDependentLookup,PrimaryFieldId,ReadOnlyField,Required
```

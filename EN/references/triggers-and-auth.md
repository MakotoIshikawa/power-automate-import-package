# Triggers, Connections, and Authentication

| Type | Status | Helper | `auth_mode` | Connection `source` | Connector action authentication |
|---|---|---|---|---|---|
| Manually trigger a flow | Import and run confirmed | `manual_trigger` | `invoker` | `Invoker` | Raw (`X-MS-APIM-Tokens`) |
| SharePoint triggers run by a user (For a selected file, and so on) | Confirmed in an exported flow | None | `invoker` | `Invoker` | Raw |
| Schedule | Trigger only confirmed in an exported flow | `recurrence_trigger` | `embedded` | Unconfirmed (inferred: `Embedded`) | Unconfirmed (inferred: `$authentication`) |
| Automated connector trigger (for example, When a file is created) | Trigger and `source` confirmed in an exported flow | `polling_trigger` | `embedded` | `Embedded` | Unconfirmed (inferred: `$authentication`) |

- When you use an unconfirmed combination, report it as unconfirmed in the design summary.
- SharePoint triggers run by a user include a region-specific `runtimeUrl`, so there is no helper. To use one, ask the requester for the `definition.json` of a flow that contains the trigger.

## Input Fields for a Manual Trigger

Pass them as a JSON schema in `properties` and `required` of `manual_trigger`.

```python
manual_trigger(
    properties={"text": {"title": "JSON", "type": "string",
                         "x-ms-content-hint": "TEXT", "x-ms-dynamically-added": True}},
    required=["text"])
```

Refer to the value with `@triggerBody()?['text']`.

## Schedule

- Specify `startTime` in UTC. 10:00 Japan time is `01:00:00.000Z`.
- `interval` is a string (`"1"`) in exported flows.

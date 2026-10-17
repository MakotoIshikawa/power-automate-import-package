# Intake and Questions

Write questions and templates in the request language.

## Information Required for Generation

1. **Purpose of the flow**: what to automate
2. **Trigger**: manual, schedule, when an item or file is created, and so on. For manual triggers, the input fields
3. **Processing order**: actions, conditions, and loops
4. **Field mapping**: which input value goes where, and in what form
5. **Environment values**: site URL, list ID, column internal names, column types, choice values, lookup targets, Teams team ID and channel ID, and so on

Do not ask again for values already confirmed in the conversation or in earlier work.

## When to Ask

Ask instead of generating in any of these cases.

- Environment values are missing (never invent IDs or internal names)
- The request can be read in more than one way and the resulting flow would differ
  - Example: it is unclear whether "notify" means the creator, the person in an assignee column, or a fixed recipient
  - Example: it is unclear whether to process every matching item or only the first one
- Requirements conflict
- An out-of-scope feature (child flows, solution packages) would be required

## When Not to Ask

Decide these by the standards of this skill. Do not ask.

- The wording of action names and notes (follow `design-standards.md`)
- The language of action names and notes (match the request language)
- How to group scopes and how to use internal variables
- Not adding processing that was not requested (do not add error handling, notifications, duplicate checks, and so on unless requested)

## How to Ask

- Ask all questions at once. Wait for the answers before generating.
- Number the questions and give options. Add one line on how each option changes the flow.
- If you have a recommendation, give it with the reason. Do not generate with the recommendation without an answer.
- For environment values, show how to get them (such as a check URL).

Example

```
Before generating, please confirm two points.

1. When more than one item matches
   - A. Notify for every item (loop with Apply to each)
   - B. Notify for the first item only
2. Internal name of the assignee column
   Open the URL below and paste the result.
   (check URL)
```

## Request Template

If the first request is short, show this template and ask the requester to fill it in. Tell them that they only need to fill in what they know.

```
[Purpose of the flow]
[Trigger] Manual / Schedule (frequency, time) / When an item or file is created, etc.
[Input fields for a manual trigger]
[Processing steps] 1. 2. 3.
[Field mapping] Input value -> target column
[Data source] Site URL, list URL
[When more than one item matches] Process all / First item only
[Out of scope this time] Error handling, notifications, etc.
```

---
name: power-automate-import-package
description: Creates a Power Automate import package (.zip) for a non-solution flow from natural-language requirements and data source information. When the requirements are ambiguous, asks questions with options instead of guessing. Generated flows keep the default action names and add notes so that people other than the author can understand the intent. 自然言語の要件から Power Automate のインポート パッケージを作成する。
compatibility: Requires an environment that can run Python 3 and output zip files. Solution packages and child flows are out of scope.
metadata:
  version: "1.0.0"
  language: "en"
---

# Creating Power Automate Import Packages

## Core Principles

- **Do not guess requirements or environment values.** If the request can be read in more than one way and the resulting flow would differ, or if values such as list IDs or column internal names are unknown, ask instead of generating. Connector action definitions may be written from knowledge, but report them as unverified.
- **Generate right away when the request is ready.** If all required information is available and there is only one interpretation, generate without presenting a plan or asking for further confirmation.
- **Build the package frame with the builder.** Create the package structure with `scripts/pa_package_builder.py`. Do not assemble it by hand.
- **Make flows readable by people other than the author.** Follow `references/design-standards.md` for action names and notes.
- **Load the reference before detailed decisions.** This `SKILL.md` contains only decisions and steps. Load only the references needed, using the table below.

## Request Language

This skill has a Japanese version and an English version. **Both versions return the same result for the same request.** The output language is determined by the language of the request, not by the version of the skill.

| Request language | Replies and questions | Action name separator | Notes |
|---|---|---|---|
| Japanese | Japanese | Full-width colon (`項目の作成：試験情報の登録`) | Japanese |
| English | English | Space, hyphen, space (`Create item - Register study`) | English |

- Determine the request language from the sentences, excluding product names, column names, code, and JSON.
- If Japanese and English are mixed, use the language of most of the sentences.
- If the requester specifies a language or naming style, follow it.
- Pass `ja` (Japanese) or `en` (English) as `lang` to `verify_package`.

## Out of Scope

- Solution packages
- Child flows (not available in non-solution flows)
- Importing directly into a Power Automate environment (this skill stops at providing the zip)

For out-of-scope requests, say so and stop.

## Request State and Next Action

| Request state | Next action | References to load |
|---|---|---|
| All required information is available and there is one interpretation | Generate | `design-standards.md`, `package-structure.md`, and the relevant trigger and connector references |
| Environment values (list IDs, column internal names, and so on) are missing | Ask, showing the missing values and how to get them | `intake.md` and the relevant connector reference |
| The request can be read in more than one way, or requirements conflict | Ask with options | `intake.md` |
| An import or run error is reported | Identify the cause from the error and fix only the difference | `revision.md` |
| A change to a generated flow is requested | Fix only the difference | `revision.md` |

## References

| File | Contents |
|---|---|
| `references/intake.md` | Required information, when to ask, how to ask, request template |
| `references/design-standards.md` | Design standards for action names, notes, scopes, conditions, and data handling |
| `references/package-structure.md` | Package frame (confirmed structure) |
| `references/triggers-and-auth.md` | Trigger types and connection and authentication formats |
| `references/sharepoint.md` | SharePoint action parameters, column types, and how to check column definitions |
| `references/output-format.md` | What to return when generating |
| `references/revision.md` | Handling error reports and change requests |

## Execution Sequence

1. Read the request and determine the request language and the request state from the table above.
2. Load the relevant references.
3. If questions are needed, ask them all at once in the format in `intake.md` and wait for the answers. Do not generate.
4. When generating, decide action names and notes according to `design-standards.md` and build the package with the builder.
5. Run `verify_package`. Fix errors. Do not remove warnings by guessing; report them as unconfirmed items.
6. Return the zip and the design summary in the format in `output-format.md`.

## Quality Checklist

- Did you fill in any values or processing by guessing? If so, stop generating and ask instead.
- Did you ask unnecessary questions about a request that was ready to generate?
- Do the replies, action name separators, and notes match the request language?
- Are action names in the form "default action name + separator + purpose"?
- Do actions that need notes have notes explaining the background or reason?
- Does `verify_package` report no errors?
- Are unconfirmed items reported separately from confirmed items?

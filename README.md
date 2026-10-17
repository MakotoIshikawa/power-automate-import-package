# 📦 power-automate-import-package

English | [日本語](README_JP.md)

An agent skill that creates a Power Automate import package (.zip) for a non-solution flow from natural-language requirements.

You describe the flow and its data sources in plain language. The skill builds the package, checks its structure, and returns it with a design summary. If the request is ambiguous, it asks you questions instead of guessing.

> [!NOTE]
> This is not an official Microsoft product.

## ✨ Features

- **Asks instead of guessing**: If a request can be read in more than one way, or values such as list IDs and column internal names are missing, the skill asks questions with options before generating anything.
- **Generates right away when ready**: If all required information is available, it generates the package without extra confirmation.
- **Readable flows**: Action names keep the default action name and add the purpose. Notes explain the background and design reasons that the name alone cannot convey.
- **Follows the request language**: The same request returns the same flow with either version of the skill. Replies, action names, and notes follow the language of the request.

  | Request language | Action name example |
  |---|---|
  | English | `Create item - Register order` |
  | Japanese | `項目の作成：注文の登録` |

- **Fewer revision rounds**: Each generated package comes with a design summary, a field mapping table, confirmed and unconfirmed points, and checks to run after import.
- **Structure check**: The included Python builder creates the package frame and detects broken expression references, invalid `runAfter` settings, duplicate action names, and missing notes before you import.

## 🧭 How It Works

```text
Request in natural language
  ↓
Determine the request language and whether the request is ready
  ├─ Missing values or ambiguous → Ask questions with options
  └─ Ready → Build the package with the builder
               ↓
             Check the structure
               ↓
             Return the zip and the design summary
               ↓
Import and test run in Power Automate
  ↓
Report errors or changes → Fix only the difference
```

## 📋 Requirements

- An environment where the agent can run Python 3 and output zip files
  - The builder uses only the Python standard library.
- A Power Automate environment where you can import packages

> [!IMPORTANT]
> Skills in Copilot in SharePoint cannot run custom code, so this skill cannot create packages there.

## 🗂 Repository Structure

```text
.
├── README.md
├── README_JP.md
├── JP/                         Japanese version
│   ├── SKILL.md
│   ├── references/
│   │   ├── design-standards.md
│   │   ├── intake.md
│   │   ├── output-format.md
│   │   ├── package-structure.md
│   │   ├── revision.md
│   │   ├── sharepoint.md
│   │   └── triggers-and-auth.md
│   └── scripts/
│       └── pa_package_builder.py
└── EN/                         English version (same structure)
```

- `SKILL.md` contains only decisions and steps. Details are in `references/` and are loaded only when needed.
- `scripts/pa_package_builder.py` is identical in both versions.
- The skill name (`name` in `SKILL.md`) is `power-automate-import-package` in both versions. Use only one version in the same agent.

## 🚀 Installation

Download the zip for the version you want from the Releases page of this repository.

| File | Version |
|---|---|
| `power-automate-import-package_EN.zip` | English |
| `power-automate-import-package_JP.zip` | Japanese |

Both versions return the same results. Choose the one you want to read and maintain.

### Copilot Studio

Use an agent created with the GitHub Copilot harness.

1. Open the agent and select the **Build** tab.
2. Select **Skills**, then **Add skill**, then **Upload a skill**.
3. Upload the zip file as it is.

### Agent Builder

Skills in Agent Builder are in preview and require your organization to be enrolled in the Microsoft Frontier Program.

1. Open or create an agent in Agent Builder.
2. On the **Configure** tab, expand **Skills** and select **Add**.
3. Upload the zip file as it is.

### Placing the Skill in a Skills Folder

Copy the `EN/` or `JP/` folder and rename it to `power-automate-import-package`. The folder name must match `name` in `SKILL.md`.

## 💬 Usage

Describe the flow and its data sources. Values that differ by environment, such as list IDs and column internal names, are required.

Example request

```text
Create a manually triggered flow that takes JSON text as input
and registers each record in the "records" array to the Orders list.

Site: https://contoso.sharepoint.com/sites/Sales
List ID: 00000000-0000-0000-0000-000000000000
Mapping:
- orderNumber -> Title
- customerName -> CustomerName
- amount -> Amount (number)
Process every record.
```

If your request is short, the skill shows the following template.

```text
[Purpose of the flow]
[Trigger] Manual / Schedule (frequency, time) / When an item or file is created, etc.
[Input fields for a manual trigger]
[Processing steps] 1. 2. 3.
[Field mapping] Input value -> target column
[Data source] Site URL, list URL
[When more than one item matches] Process all / First item only
[Out of scope this time] Error handling, notifications, etc.
```

If you don't know the list ID or column internal names, the skill shows SharePoint REST API URLs that you can open in a browser to get them.

After import, run a test and check the results against the checks in the design summary. If an error occurs, send the error message or the output of the failed action. The skill fixes only the difference and creates a new version.

## ✅ What Has Been Verified

| Item | Status |
|---|---|
| Manual trigger + SharePoint "Create item" | Import and run confirmed |
| Parent and child lists linked by a lookup column | Import and run confirmed |
| Notes stored in `description` | Confirmed in an exported flow |
| Schedule trigger | Trigger confirmed in an exported flow; not imported |
| Automated SharePoint trigger (When a file is created) | Trigger confirmed in an exported flow; not imported |
| Connector actions in scheduled or automated flows | Unconfirmed (authentication is set by inference) |
| Actions other than SharePoint "Create item" | Written from knowledge; reported as unverified |

The skill reports unverified points with each generated package.

## 🚫 Out of Scope

- Solution packages
- Child flows (not available in non-solution flows)
- Importing directly into a Power Automate environment

## ⚠️ Disclaimer

- Always test generated flows before using them in production.
- The package format is based on exported packages at the time of verification. If imports stop working, the format may have changed.
- The structure check does not guarantee a successful import.

## 🙏 Acknowledgements

The structure of `SKILL.md` (keeping the main file thin, loading references only when needed, and returning to execution when the request is ready) was inspired by Microsoft's `sharepoint-automation` skill in Copilot in SharePoint. No files from that skill are included in this repository.

## 📄 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

# Handling Error Reports and Change Requests

## How to Revise

1. From the error, determine whether the cause is the package frame (on import) or the action contents (on run).
2. Change only the difference. Do not change parts that work.
3. Create the revised package with a new version in the file name. Do not overwrite the previous file.
4. Show what changed, before and after.

## When the Cause Cannot Be Identified

- Do not change several places at once by guessing. You would not know which change worked.
- Ask the requester for the necessary information (the output of the failed action, the error message).
- If the cause still cannot be identified, ask for the `definition.json` of an existing flow that contains the action.

## When to Ask for a Sample

Do not ask for an exported flow every time. Ask only in these cases.

- The import stopped or failed
- A run error could not be fixed from the error contents
- A trigger without a helper is used, such as a SharePoint trigger run by a user

If a zip cannot be attached, ask the requester to extract it and attach `Microsoft.Flow\flows\<GUID>\definition.json`. If that cannot be attached either, ask them to change the extension to `.txt` or paste the contents.

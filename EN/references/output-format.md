# What to Return When Generating

To reduce revision rounds, return the following in this order. Write the reply in the request language.

1. **Zip file**
2. **Design summary**

| Order | Action name | Processing | Note |
|---|---|---|---|
| 1 | Get item - User data | ... | ... |

3. **Field mapping table**: input value -> target (column display name, internal name)
4. **Confirmation status**: show confirmed parts separately from unconfirmed points (`verify_package` warnings and actions written from knowledge). `verify_package` warnings are returned in English; translate them into the request language
5. **Checks after import**: values to check in a test run, with the expected results
6. **Information to send if an error occurs**
   - On import: a screenshot of the screen or the error message
   - On run: the name of the failed action and its output or error

Do not add processing that was not requested. If additional processing would help, do not add it to the flow; suggest it in one line at the end.

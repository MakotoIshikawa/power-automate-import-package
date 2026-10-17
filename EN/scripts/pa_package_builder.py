"""Builder for Power Automate non-solution flow import packages.

The package frame (manifest, ID mapping, connection references) follows the confirmed structure.
Action names and notes (memos) are checked against the design standards in SKILL.md.
This file is identical in the Japanese (JP) and English (EN) skill packages.
"""
import datetime
import json
import re
import uuid
import zipfile

WF_SCHEMA = "https://schema.management.azure.com/providers/Microsoft.Logic/schemas/2016-06-01/workflowdefinition.json#"
ICON_BASE = "https://static.powerapps.com/resource/ppcr/releases/v1.0.1818/1.0.1818.4788"
RAW_AUTH = {"value": "@json(decodeBase64(triggerOutputs().headers['X-MS-APIM-Tokens']))['$ConnectionKey']", "type": "Raw"}
EMBEDDED_AUTH = "@parameters('$authentication')"

# Action types that must have a note (memo)
MEMO_REQUIRED_TYPES = {"OpenApiConnection", "If", "Switch", "Foreach", "Scope", "ParseJson", "Query", "Select"}
REF_PATTERN = re.compile(r"\b(?:outputs|body|actions|items|result)\('([^']+)'\)")
# Naming separators: full-width colon for Japanese requests, " - " for English requests
SEPARATORS = {"ja": "：", "en": " - "}


def action_name(base, purpose, lang):
    """Build a display name: '<default action name><separator><purpose>'. lang is 'ja' or 'en'."""
    return f"{base}{SEPARATORS[lang]}{purpose}"


def action_key(display_name):
    """Convert a display name to the key used in the definition and in expressions (spaces -> _)."""
    return display_name.replace(" ", "_")


def _host(api, operation):
    return {"apiId": f"/providers/Microsoft.PowerApps/apis/shared_{api}",
            "connectionName": f"shared_{api}", "operationId": operation}


def _finish(action, run_after, memo):
    action["runAfter"] = run_after or {}
    if memo:
        action["description"] = memo
    return action


def openapi_action(api, operation, parameters, run_after=None, memo=None, auth_mode="invoker"):
    """Connector action."""
    a = {"type": "OpenApiConnection",
         "inputs": {"host": _host(api, operation), "parameters": parameters,
                    "authentication": RAW_AUTH if auth_mode == "invoker" else EMBEDDED_AUTH}}
    return _finish(a, run_after, memo)


def builtin_action(action_type, inputs=None, run_after=None, memo=None, **extra):
    """Built-in action (Compose, ParseJson, Query, Select, InitializeVariable, ...)."""
    a = {"type": action_type}
    if inputs is not None:
        a["inputs"] = inputs
    a.update(extra)
    return _finish(a, run_after, memo)


def foreach_action(items_expr, actions, run_after=None, memo=None, sequential=False):
    """Apply to each. sequential=True sets concurrency to 1."""
    a = {"type": "Foreach", "foreach": items_expr, "actions": actions}
    if sequential:
        a["runtimeConfiguration"] = {"concurrency": {"repetitions": 1}}
    return _finish(a, run_after, memo)


def condition_action(expression, actions, else_actions=None, run_after=None, memo=None):
    """Condition."""
    a = {"type": "If", "expression": expression, "actions": actions}
    if else_actions:
        a["else"] = {"actions": else_actions}
    return _finish(a, run_after, memo)


def scope_action(actions, run_after=None, memo=None):
    """Scope."""
    return _finish({"type": "Scope", "actions": actions}, run_after, memo)


def manual_trigger(properties=None, required=None, name="manual"):
    return {name: {"type": "Request", "kind": "Button", "inputs": {"schema": {
        "type": "object", "properties": properties or {}, "required": required or []}}}}


def recurrence_trigger(frequency="Week", interval="1", start_time=None, week_days=None, name="Recurrence"):
    r = {"frequency": frequency, "interval": interval}
    if start_time:
        r["startTime"] = start_time
    if week_days:
        r["schedule"] = {"weekDays": week_days}
    return {name: {"recurrence": r, "evaluatedRecurrence": dict(r), "type": "Recurrence"}}


def polling_trigger(name, api, operation, parameters, split_on, frequency="Minute", interval=1):
    r = {"frequency": frequency, "interval": interval}
    return {name: {"recurrence": r, "evaluatedRecurrence": dict(r), "splitOn": split_on,
                   "type": "OpenApiConnection",
                   "inputs": {"parameters": parameters, "host": _host(api, operation),
                              "authentication": EMBEDDED_AUTH}}}


def build_package(path, display_name, triggers, actions, connectors, account,
                  auth_mode="invoker", content_version="undefined"):
    """Create the package. connectors is {internal name: display name}, e.g. {"sharepointonline": "SharePoint"}."""
    root, flow_id = str(uuid.uuid4()), str(uuid.uuid4())
    api_keys = {x: str(uuid.uuid4()) for x in connectors}
    conn_keys = {x: str(uuid.uuid4()) for x in connectors}
    resources = {root: {"type": "Microsoft.Flow/flows", "suggestedCreationType": "New",
                        "creationType": "Existing, New, Update", "details": {"displayName": display_name},
                        "configurableBy": "User", "hierarchy": "Root",
                        "dependsOn": [*api_keys.values(), *conn_keys.values()]}}
    for api, label in connectors.items():
        icon = f"{ICON_BASE}/{api}/icon.png"
        resources[api_keys[api]] = {"id": f"/providers/Microsoft.PowerApps/apis/shared_{api}",
                                    "name": f"shared_{api}", "type": "Microsoft.PowerApps/apis",
                                    "suggestedCreationType": "Existing",
                                    "details": {"displayName": label, "iconUri": icon},
                                    "configurableBy": "System", "hierarchy": "Child", "dependsOn": []}
        resources[conn_keys[api]] = {"type": "Microsoft.PowerApps/apis/connections",
                                     "suggestedCreationType": "Existing", "creationType": "Existing",
                                     "details": {"displayName": account, "iconUri": icon},
                                     "configurableBy": "User", "hierarchy": "Child",
                                     "dependsOn": [api_keys[api]]}
    manifest = {"schema": "1.0", "details": {
        "displayName": display_name, "description": "",
        "createdTime": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        "packageTelemetryId": str(uuid.uuid4()), "creator": "N/A", "sourceEnvironment": ""},
        "resources": resources}
    source = "Invoker" if auth_mode == "invoker" else "Embedded"
    definition = {"name": flow_id, "id": f"/providers/Microsoft.Flow/flows/{flow_id}", "type": "Microsoft.Flow/flows",
                  "properties": {
                      "apiId": "/providers/Microsoft.PowerApps/apis/shared_logicflows",
                      "displayName": display_name,
                      "definition": {"$schema": WF_SCHEMA, "contentVersion": content_version,
                                     "parameters": {"$authentication": {"defaultValue": {}, "type": "SecureObject"},
                                                    "$connections": {"defaultValue": {}, "type": "Object"}},
                                     "triggers": triggers, "actions": actions, "outputs": {}},
                      "connectionReferences": {f"shared_{api}": {
                          "connectionName": uuid.uuid4().hex, "source": source,
                          "id": f"/providers/Microsoft.PowerApps/apis/shared_{api}", "tier": "NotSpecified",
                          "apiName": api, "isProcessSimpleApiReferenceConversionAlreadyDone": False}
                          for api in connectors},
                      "flowFailureAlertSubscribed": False, "isManaged": False}}

    def dump(x):
        return json.dumps(x, ensure_ascii=False, indent=2)

    base = f"Microsoft.Flow/flows/{root}"
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("manifest.json", dump(manifest))
        z.writestr("Microsoft.Flow/flows/manifest.json",
                   dump({"packageSchemaVersion": "1.0", "flowAssets": {"assetPaths": [root]}}))
        z.writestr(f"{base}/definition.json", dump(definition))
        z.writestr(f"{base}/apisMap.json", dump({f"shared_{x}": api_keys[x] for x in connectors}))
        z.writestr(f"{base}/connectionsMap.json", dump({f"shared_{x}": conn_keys[x] for x in connectors}))
    return root


def _children(a):
    groups = []
    if isinstance(a.get("actions"), dict):
        groups.append(a["actions"])
    if isinstance(a.get("else"), dict):
        groups.append(a["else"].get("actions", {}))
    for c in (a.get("cases") or {}).values():
        groups.append(c.get("actions", {}))
    if isinstance(a.get("default"), dict):
        groups.append(a["default"].get("actions", {}))
    return groups


def _walk_groups(actions):
    yield actions
    for a in actions.values():
        for g in _children(a):
            yield from _walk_groups(g)


def _strings(obj):
    if isinstance(obj, str):
        yield obj
    elif isinstance(obj, dict):
        for v in obj.values():
            yield from _strings(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from _strings(v)


def verify_package(path, lang):
    """Check the package. lang is the language of the request: 'ja' or 'en'.

    Raises AssertionError when the confirmed structure or expression references are broken.
    Returns a list of warnings for deviations from the design standards and unconfirmed combinations.
    Passing this check does not guarantee a successful import.
    """
    assert lang in SEPARATORS, "lang must be 'ja' or 'en'"
    sep_key = action_key(SEPARATORS[lang])
    warnings = []
    with zipfile.ZipFile(path) as z:
        for n in z.namelist():
            json.loads(z.read(n))
        m = json.loads(z.read("manifest.json"))
        roots = [k for k, v in m["resources"].items() if v["type"] == "Microsoft.Flow/flows"]
        assert len(roots) == 1, "There must be exactly one flow resource"
        root = roots[0]
        base = f"Microsoft.Flow/flows/{root}/"
        fm = json.loads(z.read("Microsoft.Flow/flows/manifest.json"))
        assert fm["flowAssets"]["assetPaths"] == [root], "assetPaths does not match the resource key"
        for f in ("definition.json", "apisMap.json", "connectionsMap.json"):
            assert base + f in z.namelist(), f"{f} is not under the flow folder"
        assert "id" not in m["resources"][root] and "name" not in m["resources"][root], "The flow resource has id / name"
        for dep in m["resources"][root]["dependsOn"]:
            assert dep in m["resources"], "dependsOn points to a missing resource"
        for f in ("apisMap.json", "connectionsMap.json"):
            for v in json.loads(z.read(base + f)).values():
                assert v in m["resources"], f"A value in {f} is not a manifest resource key"
        d = json.loads(z.read(base + "definition.json"))

    assert d["name"] != root, "definition name must differ from the folder name"
    p = d["properties"]
    refs = p["connectionReferences"]
    df = p["definition"]
    sources = {r["source"] for r in refs.values()}
    types = {t["type"] for t in df["triggers"].values()}

    all_keys, all_actions = set(), []
    for group in _walk_groups(df["actions"]):
        for key, a in group.items():
            assert key not in all_keys, f"Duplicate action name: {key}"
            all_keys.add(key)
            all_actions.append((key, a))
            for dep in a.get("runAfter", {}):
                assert dep in group, f"runAfter of {key} is not in the same level: {dep}"

    for key, a in all_actions:
        assert " " not in key, f"Key contains a space (replace with _): {key}"
        if sep_key not in key:
            warnings.append(f"Name does not follow the naming standard for '{lang}' (<default name>{SEPARATORS[lang]}<purpose>): {key}")
        if a.get("type") in MEMO_REQUIRED_TYPES and not a.get("description"):
            warnings.append(f"Missing note: {key}")

    for key, a in all_actions:
        body = {k: v for k, v in a.items() if k not in ("description", "actions", "else", "cases", "default")}
        for s in _strings(body):
            for ref in REF_PATTERN.findall(s):
                assert ref in all_keys, f"Expression in {key} refers to a missing action: {ref}"

    has_api = any(a.get("type") == "OpenApiConnection" for _, a in all_actions)
    if types == {"Request"}:
        if refs:
            assert sources == {"Invoker"}, f"Manual trigger but source is {sources}"
        for key, a in all_actions:
            if a.get("type") == "OpenApiConnection":
                auth = a["inputs"]["authentication"]
                assert isinstance(auth, dict) and auth.get("type") == "Raw", f"{key}: manual trigger requires Raw authentication"
    for t in df["triggers"].values():
        if t["type"] == "OpenApiConnection":
            assert t["inputs"]["authentication"] == EMBEDDED_AUTH and sources == {"Embedded"}, "Automated trigger: authentication or source differs from the exported sample"
            assert "splitOn" in t and "recurrence" in t, "Automated trigger requires splitOn and recurrence"
            if has_api:
                warnings.append("Automated trigger + connector action: action authentication is unconfirmed (set by inference)")
    if "Recurrence" in types and refs:
        warnings.append("Schedule + connector: connection source and action authentication are unconfirmed (set by inference)")
    if not refs:
        warnings.append("Package without connectors: manifest shape is unconfirmed")
    return warnings

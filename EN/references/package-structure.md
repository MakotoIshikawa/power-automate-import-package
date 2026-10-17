# Package Frame (Confirmed)

Created by `build_package` in `scripts/pa_package_builder.py`. This reference is for changing the builder or investigating an import that stops.

```text
manifest.json
Microsoft.Flow/flows/manifest.json
Microsoft.Flow/flows/<GUID-A>/definition.json
Microsoft.Flow/flows/<GUID-A>/apisMap.json
Microsoft.Flow/flows/<GUID-A>/connectionsMap.json
```

- The flow resource key in the top-level `manifest.json`, `flowAssets.assetPaths`, and the folder name are the same GUID-A.
- The `name` in `definition.json` and the end of its `id` are GUID-B, which differs from GUID-A.
- The flow resource has no `id` or `name`. API resources have them.
- The values in `apisMap.json` and `connectionsMap.json` are the corresponding resource keys in the top-level `manifest.json`.
- Do not create `metadata`. It holds source-specific values such as the creator ID, and the import succeeded without it.
- Folder-only entries in the zip are not needed.
- A version assembled from memory in a different format stopped at "Importing package" on the import screen.

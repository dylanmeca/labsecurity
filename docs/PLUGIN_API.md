# Labsecurity 2.0 Plugin API

## Minimum Contract

A plugin folder contains `manifest.json` and the Python file specified in `entrypoint`, which defines `run(ctx)`.

```json
{
  "id": "auxiliary/custom/my_plugin",
  "description": "My demonstration plugin",
  "version": "1.0.0",
  "author": "Your Name",
  "entrypoint": "plugin.py:run",
  "options": [
    {"name": "TARGET", "type": "string", "required": true, "description": "Target"},
    {"name": "TIMEOUT", "type": "integer", "default": 3, "required": false,
     "description": "Timeout seconds"}
  ],
  "commands": []
}
```

- `id` must be a lowercase path separated by `/` consisting of at least two segments, for example `auxiliary/scanner/port_test`. All segments accept `[a-z][a-z0-9_]*`.
- `entrypoint` points to a `.py` file **in the same folder** and to a function: `plugin.py:run`.
- `options` and `commands` are lists, even when empty.
- The module’s function takes **one** argument: `run(ctx)`.
- The function for an additional command takes **two** arguments: `my_command(ctx, argv)`; `argv` is a list of strings already separated by `shlex`.

## `ctx` Methods

| Method | Description |
| --- | --- |
| `ctx.get(“NAME”, default=None)` | Returns an option converted to its declared type |
| `ctx.info(message)` | Displays `[*]` in blue |
| `ctx.success(message)` | Prints `[+]` in green |
| `ctx.warning(message)` | Prints `[!]` in yellow |
| `ctx.error(message)` | Prints `[-]` in red |
| `ctx.print(message)` | Plain text without interpreting rich markup |
| `ctx.options` | Copy of the plugin’s options; does not alter internal settings |
| `ctx.plugin_id` | Module identifier |

If `run()` returns a value other than `None`, the console displays it upon completion. Any exception is raised as an error, without closing the console.

## Option Types

`string`, `integer`, `port` (1–65535), `boolean` (true/false, yes/no, 1/0), `url` (http/https), `choice` (with `choices: [“a”, “b”]`). Required options cannot be executed if they are missing. `unset` restores the default value. `set` is validated before being applied.

## Added Commands

```json
“commands”: [
  {“name”: “greet”, “description”: “A greeting”, ‘entrypoint’: “plugin.py:greet”}
]
```

The command exists globally and does not require selecting a module. Names that conflict with the core or another plugin are ignored, with a visible warning in `plugins`. There is no automatic execution during `search`, `show`, `reload`, or when the console starts up.

## Advanced Organization

Plugins are loaded as private Python packages. You can create `helpers.py` and import it from `plugin.py`:

```python
from .helpers import helper
```

To reload changes from Labsecurity, run `reload`. Plugins share the interpreter and its permissions. A malicious plugin can read or modify user files; only run reviewed code.

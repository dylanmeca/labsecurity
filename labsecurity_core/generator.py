"""Scaffold new plugins and wrap standalone legacy Python scripts."""
from __future__ import annotations

import ast
import json
import re
import shutil
from pathlib import Path

from .models import PluginError
from .registry import IDENTIFIER

PLUGIN_TEMPLATE = '''"""Custom Labsecurity plugin. Runs ONLY when the operator selects and runs it."""


def run(ctx):
    """ctx.get('TARGET'), ctx.info(), ctx.success(), ctx.warning(), ctx.error()."""
    target = ctx.get("TARGET")
    ctx.info(f"Starting plugin for {target}")
    # TODO: implement your Python tool here.
    ctx.success("Plugin executed. Replace this example with your own logic.")


# Example custom top-level command enabled in manifest.json:
# def my_command(ctx, argv):
#     ctx.success(f"Custom command arguments: {argv}")
'''

LEGACY_TEMPLATE = '''"""Adapter for an existing Python script defining run(target, port) or run(target)."""
from __future__ import annotations

import inspect
from . import legacy_script


def run(ctx):
    """Calls the original script without modifying its implementation."""
    callback = getattr(legacy_script, "run", None)
    if not callable(callback):
        raise RuntimeError("Legacy script must expose callable run(...)")
    signature = inspect.signature(callback)
    kwargs = {}
    for name, param in signature.parameters.items():
        if param.kind not in (inspect.Parameter.POSITIONAL_OR_KEYWORD, inspect.Parameter.KEYWORD_ONLY):
            raise RuntimeError(f"Unsupported legacy argument: {name}")
        if name.lower() in {"target", "host", "rhost", "url", "domain", "ip"}:
            value = ctx.get("TARGET")
        elif name.lower() in {"port", "rport"}:
            value = ctx.get("PORT")
        elif param.default is not inspect.Parameter.empty:
            continue
        else:
            raise RuntimeError(f"Cannot map legacy argument: {name}")
        if value is None and param.default is inspect.Parameter.empty:
            raise ValueError(f"Set the required option for argument: {name}")
        if value is not None:
            kwargs[name] = value
    ctx.info("Running imported script (its own stdout is displayed below)")
    return callback(**kwargs)
'''


def _validate_segments(*segments: str) -> None:
    if not all(IDENTIFIER.fullmatch(p) for p in segments):
        raise PluginError("Names must be lowercase: a-z, 0-9 or _, starting with a letter")


def _write_plugin(root: Path, kind: str, category: str, name: str, description: str,
                  author: str, source: Path | None) -> Path:
    _validate_segments(kind, category, name)
    base = root / kind / category / name
    if base.exists():
        raise PluginError(f"Plugin directory already exists: {base}")
    root.mkdir(parents=True, exist_ok=True)
    base.mkdir(parents=True)
    try:
        manifest = {
            "id": f"{kind}/{category}/{name}",
            "description": description,
            "version": "1.0.0",
            "author": author,
            "entrypoint": "plugin.py:run",
            "options": (
                [
                    {"name": "TARGET", "type": "string", "required": False,
                     "description": "Host, domain, URL or other target used by the imported script"},
                    {"name": "PORT", "type": "port", "required": False,
                     "description": "Port used by the imported script"},
                ] if source else [
                    {"name": "TARGET", "type": "string", "required": True,
                     "description": "Value passed to your plugin"},
                ]
            ),
            "commands": [],
        }
        (base / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
        (base / "__init__.py").write_text('"""Plugin package."""\n', encoding="utf-8")
        (base / "plugin.py").write_text(LEGACY_TEMPLATE if source else PLUGIN_TEMPLATE, encoding="utf-8")
        if source is not None:
            shutil.copyfile(source, base / "legacy_script.py")
    except Exception:
        shutil.rmtree(base)
        raise
    return base


def create_plugin(root: Path, name: str, kind: str = "auxiliary", category: str = "custom",
                  author: str = "Community", description: str = "Custom Labsecurity plugin") -> Path:
    return _write_plugin(root, kind, category, name, description, author, None)


def import_script(root: Path, source: Path, name: str | None = None,
                  kind: str = "auxiliary", category: str = "legacy") -> Path:
    source = source.expanduser().resolve()
    if not source.is_file() or source.suffix != ".py":
        raise PluginError("Specify an existing .py file")
    # Read-only AST inspection: do not import the source as part of the import operation.
    try:
        tree = ast.parse(source.read_text(encoding="utf-8"))
    except (SyntaxError, UnicodeDecodeError) as exc:
        raise PluginError(f"Invalid Python source: {exc}") from exc
    if not any(isinstance(node, ast.FunctionDef) and node.name == "run" for node in tree.body):
        raise PluginError("Imported scripts must define a top-level function run(...) ")
    name = name or re.sub(r"[^a-z0-9_]+", "_", source.stem.lower()).strip("_")
    if not name or not name[0].isalpha():
        name = "tool_" + name
    return _write_plugin(root, kind, category, name, f"Imported from {source.name}",
                         "Imported script", source)


def install_plugin(root: Path, source: Path) -> Path:
    """Install a complete local plugin folder; never execute its Python code here."""
    source = source.expanduser().resolve()
    if not source.is_dir() or not (source / "manifest.json").is_file():
        raise PluginError("Provide a plugin folder containing manifest.json")
    # Only explicit, local plugin folders; no automatic download or remote execution.
    from .registry import Registry
    try:
        parsed = Registry(root)._parse(source / "manifest.json")
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        raise PluginError(f"Invalid plugin manifest: {exc}") from exc
    for path in source.rglob("*"):
        if path.is_symlink():
            raise PluginError("Installation of plugins with symbolic links is not supported")
    destination = root.joinpath(*parsed.id.split("/"))
    if destination.exists():
        raise PluginError(f"Plugin already installed: {parsed.id}")
    if destination.resolve().is_relative_to(source):
        raise PluginError("Cannot install a plugin into one of its own subdirectories")
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(source, destination, ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".git", ".venv"))
    return destination

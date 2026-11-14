"""Plugin discovery from manifest JSON without importing or executing plugin code."""
from __future__ import annotations

import json
import re
from pathlib import Path
from .models import ExtensionCommand, Option, Plugin, PluginError

IDENTIFIER = re.compile(r"^[a-z][a-z0-9_]*$")
FUNCTION = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
CORE_COMMANDS = frozenset({
    "help", "?", "banner", "search", "use", "info", "show", "set", "unset", "run", "exploit",
    "back", "reload", "plugins", "plugin", "history", "clear", "cls", "exit", "quit", "resource",
})


def parse_entrypoint(value: str, path: Path) -> tuple[Path, str]:
    """Only relative, single Python filenames; avoid traversing out of plugin folder."""
    if not isinstance(value, str) or value.count(":") != 1:
        raise PluginError("entrypoint must be 'plugin.py:function'")
    filename, function = value.split(":")
    if not filename.endswith(".py") or not IDENTIFIER.fullmatch(filename[:-3]):
        raise PluginError(f"Invalid entrypoint filename: {filename!r}")
    if not FUNCTION.fullmatch(function):
        raise PluginError(f"Invalid entrypoint function: {function!r}")
    script = (path / filename).resolve()
    if script.parent != path.resolve() or not script.is_file():
        raise PluginError(f"Entrypoint Python file not found: {filename}")
    return script, function


class Registry:
    def __init__(self, plugin_root: Path):
        self.plugin_root = plugin_root
        self.modules: dict[str, Plugin] = {}
        self.commands: dict[str, tuple[Plugin, ExtensionCommand]] = {}
        self.errors: list[str] = []
        self.refresh()

    def refresh(self) -> None:
        self.modules.clear()
        self.commands.clear()
        self.errors.clear()
        if not self.plugin_root.exists():
            return
        for manifest_path in sorted(self.plugin_root.rglob("manifest.json")):
            try:
                if not manifest_path.resolve().is_relative_to(self.plugin_root.resolve()):
                    raise PluginError("Manifest is outside the plugins directory")
                plugin = self._parse(manifest_path)
                if plugin.id in self.modules:
                    raise PluginError(f"Duplicate module id: {plugin.id}")
                self.modules[plugin.id] = plugin
            except (PluginError, OSError, ValueError, json.JSONDecodeError) as exc:
                self.errors.append(f"{manifest_path.relative_to(self.plugin_root)}: {exc}")
        for plugin in self.modules.values():
            for name, command in plugin.commands.items():
                if name in CORE_COMMANDS:
                    self.errors.append(f"{plugin.id}: command '{name}' is reserved by the core")
                elif name in self.commands:
                    self.errors.append(f"{plugin.id}: duplicate extension command '{name}'")
                else:
                    self.commands[name] = (plugin, command)

    def _parse(self, path: Path) -> Plugin:
        raw = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(raw, dict):
            raise PluginError("Manifest must contain a JSON object")
        module_id = raw.get("id")
        if not isinstance(module_id, str) or len(module_id.split("/")) < 2 or not all(
            IDENTIFIER.fullmatch(item) for item in module_id.split("/")
        ):
            raise PluginError("id must be lowercase slash-separated segments, e.g. auxiliary/scanner/ports")
        module_path = path.parent
        parse_entrypoint(raw.get("entrypoint", "plugin.py:run"), module_path)
        options: dict[str, Option] = {}
        raw_options = raw.get("options", [])
        if not isinstance(raw_options, list):
            raise PluginError("options must be a JSON array")
        for item in raw_options:
            option = Option.from_dict(item)
            if option.name in options:
                raise PluginError(f"Duplicate option {option.name}")
            options[option.name] = option
        commands: dict[str, ExtensionCommand] = {}
        raw_commands = raw.get("commands", [])
        if not isinstance(raw_commands, list):
            raise PluginError("commands must be a JSON array")
        for item in raw_commands:
            if not isinstance(item, dict):
                raise PluginError("Each command must be a JSON object")
            name = item.get("name")
            if not isinstance(name, str) or not IDENTIFIER.fullmatch(name):
                raise PluginError(f"Invalid command name: {name!r}")
            parse_entrypoint(item.get("entrypoint", ""), module_path)
            if name in commands:
                raise PluginError(f"Duplicate command {name}")
            commands[name] = ExtensionCommand(name, str(item.get("description", "")), item["entrypoint"])
        return Plugin(
            id=module_id,
            description=str(raw.get("description", "")),
            path=module_path,
            entrypoint=raw.get("entrypoint", "plugin.py:run"),
            version=str(raw.get("version", "1.0.0")),
            author=str(raw.get("author", "Community")),
            options=options,
            commands=commands,
        )

    def search(self, query: str = "") -> list[Plugin]:
        q = query.lower().strip()
        return [p for p in self.modules.values() if q in p.id.lower() or q in p.description.lower()]

    def resolve(self, selector: str) -> Plugin:
        if selector in self.modules:
            return self.modules[selector]
        # numeric indices correspond to the last search, maintained by the console
        matches = [p for p in self.modules.values() if p.id.endswith("/" + selector)]
        if len(matches) == 1:
            return matches[0]
        if len(matches) > 1:
            raise PluginError("Ambiguous module. Use its full path: " + ", ".join(p.id for p in matches))
        raise PluginError(f"Module not found: {selector}")

"""Declarative plugin contracts and typed plugin option values."""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit


class PluginError(Exception):
    """Invalid manifest, option, command or plugin implementation."""


@dataclass(frozen=True)
class Option:
    name: str
    description: str = ""
    type: str = "string"
    required: bool = False
    default: Any = None
    choices: tuple[str, ...] = ()

    @classmethod
    def from_dict(cls, raw: dict) -> "Option":
        if not isinstance(raw, dict) or not isinstance(raw.get("name"), str):
            raise PluginError("Each option must be an object with a name")
        name = raw["name"].upper()
        if not name.isidentifier() or name.startswith("_"):
            raise PluginError(f"Invalid option name: {name!r}")
        kind = raw.get("type", "string")
        if kind not in {"string", "integer", "port", "boolean", "url", "choice"}:
            raise PluginError(f"Unsupported option type for {name}: {kind}")
        choices = raw.get("choices", [])
        if not isinstance(choices, list) or not all(isinstance(c, str) for c in choices):
            raise PluginError(f"Option {name}: choices must be a list of strings")
        if kind == "choice" and not choices:
            raise PluginError(f"Option {name}: choices cannot be empty")
        opt = cls(name=name, description=str(raw.get("description", "")),
                  type=kind, required=bool(raw.get("required", False)),
                  default=raw.get("default"), choices=tuple(choices))
        if opt.default is not None:
            opt.convert(opt.default)
        return opt

    def convert(self, value: Any) -> Any:
        if value is None or (isinstance(value, str) and not value.strip()):
            return None
        if self.type in {"integer", "port"}:
            try:
                converted = int(value)
            except (TypeError, ValueError) as exc:
                raise PluginError(f"{self.name} must be an integer") from exc
            if self.type == "port" and not 1 <= converted <= 65535:
                raise PluginError(f"{self.name} must be between 1 and 65535")
            return converted
        if self.type == "boolean":
            if isinstance(value, bool):
                return value
            lowered = str(value).lower()
            if lowered not in {"true", "false", "yes", "no", "1", "0", "on", "off"}:
                raise PluginError(f"{self.name}: expected true/false")
            return lowered in {"true", "yes", "1", "on"}
        text = str(value).strip()
        if self.type == "url":
            parts = urlsplit(text)
            if parts.scheme not in {"http", "https"} or not parts.netloc:
                raise PluginError(f"{self.name}: expected an http(s) URL")
        if self.type == "choice" and text not in self.choices:
            raise PluginError(f"{self.name}: choose one of {', '.join(self.choices)}")
        return text

    def value_or_default(self) -> Any:
        return self.convert(self.default)


@dataclass(frozen=True)
class ExtensionCommand:
    name: str
    description: str
    entrypoint: str


@dataclass
class Plugin:
    id: str
    description: str
    path: Path
    entrypoint: str
    version: str = "1.0.0"
    author: str = "Community"
    options: dict[str, Option] = field(default_factory=dict)
    commands: dict[str, ExtensionCommand] = field(default_factory=dict)

    @property
    def kind(self) -> str:
        return self.id.split("/")[0]

    def defaults(self) -> dict[str, Any]:
        return {name: option.value_or_default() for name, option in self.options.items()}


class PluginContext:
    """Stable API presented to plugins. Do not import framework internals in plugins."""

    def __init__(self, plugin: Plugin, options: dict[str, Any], output: Any):
        self.plugin_id = plugin.id
        self.options = dict(options)
        self._output = output

    def get(self, name: str, default: Any = None) -> Any:
        return self.options.get(name.upper(), default)

    def info(self, message: object) -> None:
        self._output.info(str(message))

    def success(self, message: object) -> None:
        self._output.success(str(message))

    def warning(self, message: object) -> None:
        self._output.warning(str(message))

    def error(self, message: object) -> None:
        self._output.error(str(message))

    def print(self, message: object = "") -> None:
        self._output.text(str(message))

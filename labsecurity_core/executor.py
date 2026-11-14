"""On-demand Python plugin runner; plugin discovery is declarative and side-effect free."""
from __future__ import annotations

import hashlib
import importlib.util
import sys
import types
from typing import Any

from .models import Plugin, PluginContext, PluginError
from .registry import parse_entrypoint


class Executor:
    def __init__(self, output: Any):
        self.output = output

    def _load(self, plugin: Plugin, entrypoint: str) -> Any:
        # Reuse an isolated namespace for the plugin folder. Relative imports work.
        script, function = parse_entrypoint(entrypoint, plugin.path)
        digest = hashlib.sha256(str(plugin.path.resolve()).encode("utf-8")).hexdigest()[:16]
        parent_name = f"_labsecurity_plugin_{digest}"
        module_name = f"{parent_name}.{script.stem}"
        if parent_name not in sys.modules:
            package = types.ModuleType(parent_name)
            package.__path__ = [str(plugin.path)]
            package.__package__ = parent_name
            sys.modules[parent_name] = package
        module = sys.modules.get(module_name)
        if module is None:
            spec = importlib.util.spec_from_file_location(module_name, script)
            if spec is None or spec.loader is None:
                raise PluginError(f"Cannot load Python file {script.name}")
            module = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = module
            try:
                # Read source afresh: reload works even when file mtime/size has not changed.
                with open(script, "rb") as handle:
                    source = handle.read()
                exec(compile(source, str(script), "exec"), module.__dict__)
            except Exception:
                sys.modules.pop(module_name, None)
                raise
        callback = getattr(module, function, None)
        if not callable(callback):
            raise PluginError(f"Missing function {function} in {script.name}")
        return callback

    def execute(self, plugin: Plugin, values: dict, entrypoint: str | None = None, args: list[str] | None = None) -> Any:
        callback = self._load(plugin, entrypoint or plugin.entrypoint)
        ctx = PluginContext(plugin, values, self.output)
        # Optional command extensions take (ctx, argv); module entrypoint takes (ctx).
        return callback(ctx, args or []) if entrypoint is not None else callback(ctx)

    @staticmethod
    def forget(plugin: Plugin) -> None:
        digest = hashlib.sha256(str(plugin.path.resolve()).encode("utf-8")).hexdigest()[:16]
        prefix = f"_labsecurity_plugin_{digest}"
        for name in list(sys.modules):
            if name == prefix or name.startswith(prefix + "."):
                sys.modules.pop(name, None)

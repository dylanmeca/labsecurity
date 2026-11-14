"""Interactive shell with Metasploit-like commands, search, configuration and completion."""
from __future__ import annotations

import shlex
import sys
from pathlib import Path
from typing import Any

from prompt_toolkit import PromptSession
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.history import FileHistory
from prompt_toolkit.styles import Style
from rich.console import Console
from rich.text import Text

from .executor import Executor
from .generator import create_plugin, import_script, install_plugin
from .models import Plugin, PluginError
from .registry import CORE_COMMANDS, Registry
from .ui import Output


HELP = """Core commands
=============
  help                 Show this help
  search [keyword]     Search installed modules
  use <module|index>   Select a module (index from last search)
  info [module]        Show module details
  show modules         List all modules
  show options         Show selected module options
  show commands        List console and plugin commands
  set NAME VALUE       Set module option
  unset NAME           Reset module option to its default
  run                  Execute the selected module
  back                 Leave the selected module
  reload               Rediscover plugins and reload source files
  plugins              Show plugin inventory and discovery errors
  plugin create [name] [kind] [category]   Generate a plugin (wizard if no name)
  plugin import <path.py> [name]           Import an existing script with run(...)
  plugin install <folder>                  Install a complete local plugin
  history              Display this session's entered commands
  banner               Redisplay the welcome banner
  clear                Clear the screen
  exit                 Exit Labsecurity

Commands are case insensitive; option names are case insensitive. Quote values with spaces.
Use only plugins and targets you are authorized to access.
"""


class LabsecurityCompleter(Completer):
    def __init__(self, app: "LabsecurityConsole") -> None:
        self.app = app

    def get_completions(self, document, complete_event):
        text = document.text_before_cursor
        tokens = text.split()
        trailing = text.endswith(" ")
        if not tokens or (len(tokens) == 1 and not trailing):
            values = set(CORE_COMMANDS) | set(self.app.registry.commands)
            needle = tokens[0].lower() if tokens else ""
        elif tokens[0].lower() in {"use", "info"}:
            values = self.app.registry.modules.keys()
            needle = "" if trailing else tokens[-1]
        elif tokens[0].lower() in {"set", "unset"} and self.app.selected is not None and len(tokens) <= 2:
            values = self.app.selected.options.keys()
            needle = "" if trailing else tokens[-1]
        elif tokens[0].lower() == "show" and len(tokens) <= 2:
            values = {"options", "modules", "commands"}
            needle = "" if trailing else tokens[-1]
        elif tokens[0].lower() == "plugin" and len(tokens) <= 2:
            values = {"create", "import", "install"}
            needle = "" if trailing else tokens[-1]
        else:
            return
        for value in sorted(values):
            if str(value).lower().startswith(needle.lower()):
                yield Completion(str(value), start_position=-len(needle))


class LabsecurityConsole:
    def __init__(self, root: Path, output: Output | None = None):
        self.root = Path(root).resolve()
        self.registry = Registry(self.root / "plugins")
        self.output = output or Output()
        self.executor = Executor(self.output)
        self.selected: Plugin | None = None
        self.settings: dict[str, dict[str, Any]] = {}
        self.last_search: list[Plugin] = []
        self.session_history: list[str] = []
        self.running = True
        self.session: PromptSession | None = None
        self._session_style = Style.from_dict({"prompt": "bold ansibrightblue", "module": "bold ansired"})

    def cmdloop(self) -> None:
        # Prompt Toolkit gives persistent interactive history, Ctrl+C and TAB completion.
        history_file = Path.home() / ".labsecurity" / "history"
        try:
            history_file.parent.mkdir(parents=True, exist_ok=True)
            history = FileHistory(str(history_file))
        except OSError:
            from prompt_toolkit.history import InMemoryHistory
            history = InMemoryHistory()
        self.session = PromptSession(history=history, completer=LabsecurityCompleter(self),
                                     complete_while_typing=False, style=self._session_style)
        self.output.banner(self.registry)
        for issue in self.registry.errors:
            self.output.warning(issue)
        while self.running:
            try:
                label = "labsecurity" + (f" ({self.selected.id})" if self.selected else "")
                prompt = HTML(f'<prompt>{label.split(" (")[0]}</prompt>'
                              + (f' <module>({self.selected.id})</module>' if self.selected else "")
                              + '<prompt> &gt; </prompt>')
                line = self.session.prompt(prompt)
                self.execute_line(line)
            except (EOFError, SystemExit):
                self.running = False
            except KeyboardInterrupt:
                self.output.text("^C (type 'exit' to quit)")
        self.output.info("Goodbye.")

    def execute_line(self, line: str) -> None:
        line = line.strip()
        if not line:
            return
        self.session_history.append(line)
        try:
            args = shlex.split(line)
            if not args:
                return
            command = args.pop(0).lower()
            if command in {"exit", "quit"}:
                self.running = False
            elif command in {"help", "?"}:
                self.output.text(HELP)
            elif command == "banner":
                self.output.banner(self.registry)
            elif command == "search":
                self.last_search = self.registry.search(" ".join(args))
                self.output.module_table(self.last_search)
            elif command == "use":
                self._use(args)
            elif command == "info":
                self._info(args)
            elif command == "show":
                self._show(args)
            elif command == "set":
                self._set(args)
            elif command == "unset":
                self._unset(args)
            elif command in {"run", "exploit"}:
                self._run()
            elif command == "back":
                self.selected = None
            elif command == "plugins":
                self._plugins()
            elif command == "plugin":
                self._plugin(args)
            elif command == "reload":
                self._reload()
            elif command == "history":
                for index, cmd in enumerate(self.session_history, 1):
                    self.output.text(f"{index:>4}  {cmd}")
            elif command in {"clear", "cls"}:
                self.output.console.clear()
            elif command in self.registry.commands:
                plugin, ext = self.registry.commands[command]
                self.output.info(f"Running extension command '{command}' ({plugin.id})")
                self.executor.execute(plugin, plugin.defaults(), ext.entrypoint, args)
            else:
                self.output.error(f"Unknown command: {command}. Type 'help'.")
        except (PluginError, ValueError, OSError, ImportError, RuntimeError) as exc:
            self.output.error(str(exc))
        except KeyboardInterrupt:
            self.output.warning("Operation cancelled by user")
        except Exception as exc:
            self.output.error(f"Plugin or command failed ({type(exc).__name__}): {exc}")
            self.output.info("Use 'info' to inspect the module; untrusted plugins can execute code.")

    def _use(self, args: list[str]) -> None:
        if len(args) != 1:
            raise PluginError("Usage: use <module|index>")
        target = args[0]
        if target.isdigit():
            number = int(target)
            if not 0 <= number < len(self.last_search):
                raise PluginError("Unknown search result index; run 'search' first")
            plugin = self.last_search[number]
        else:
            plugin = self.registry.resolve(target)
        self.selected = plugin
        self.settings.setdefault(plugin.id, plugin.defaults())
        self.output.success(f"Using module {plugin.id}")

    def _info(self, args: list[str]) -> None:
        if len(args) > 1:
            raise PluginError("Usage: info [module]")
        plugin = self.registry.resolve(args[0]) if args else self._require_selected()
        self.output.text(f"\nName:        {plugin.id}")
        self.output.text(f"Description: {plugin.description}")
        self.output.text(f"Version:     {plugin.version}")
        self.output.text(f"Author:      {plugin.author}")
        self.output.text(f"Location:    {plugin.path.relative_to(self.root)}")
        self.output.options_table(plugin, self.settings.get(plugin.id, plugin.defaults()))

    def _show(self, args: list[str]) -> None:
        if len(args) != 1 or args[0].lower() not in {"options", "modules", "commands"}:
            raise PluginError("Usage: show options|modules|commands")
        selected = args[0].lower()
        if selected == "modules":
            self.last_search = self.registry.search()
            self.output.module_table(self.last_search, "Available Modules")
        elif selected == "options":
            plugin = self._require_selected()
            self.output.options_table(plugin, self.settings[plugin.id])
        else:
            self.output.text(HELP)
            if self.registry.commands:
                self.output.text("\nPlugin extension commands\n=========================")
                for name, (module, ext) in sorted(self.registry.commands.items()):
                    self.output.text(f"  {name:<18} {ext.description} [{module.id}]")

    def _set(self, args: list[str]) -> None:
        plugin = self._require_selected()
        if len(args) < 2:
            raise PluginError("Usage: set NAME VALUE")
        name = args[0].upper()
        if name not in plugin.options:
            raise PluginError(f"Unknown option {name}. Type 'show options'.")
        value = plugin.options[name].convert(" ".join(args[1:]))
        self.settings[plugin.id][name] = value
        self.output.success(f"{name} => {value}")

    def _unset(self, args: list[str]) -> None:
        plugin = self._require_selected()
        if len(args) != 1:
            raise PluginError("Usage: unset NAME")
        name = args[0].upper()
        if name not in plugin.options:
            raise PluginError(f"Unknown option {name}")
        value = plugin.options[name].value_or_default()
        self.settings[plugin.id][name] = value
        self.output.success(f"{name} => {value}")

    def _run(self) -> None:
        plugin = self._require_selected()
        values = self.settings[plugin.id]
        missing = [name for name, spec in plugin.options.items() if spec.required and values.get(name) is None]
        if missing:
            raise PluginError("Required options missing: " + ", ".join(missing))
        self.output.info(f"Executing {plugin.id}...")
        result = self.executor.execute(plugin, values)
        if result is not None:
            self.output.text(str(result))
        self.output.success("Module finished")

    def _plugins(self) -> None:
        self.output.info(f"{len(self.registry.modules)} discovered plugins, "
                         f"{len(self.registry.commands)} extension commands")
        for module in self.registry.modules.values():
            self.output.text(f"  {module.id}")
        for error in self.registry.errors:
            self.output.warning(error)

    def _plugin(self, args: list[str]) -> None:
        if not args or args[0].lower() not in {"create", "import", "install"}:
            raise PluginError("Usage: plugin create [name] [kind] [category] | plugin import PATH.py [name] | plugin install FOLDER")
        subcommand = args.pop(0).lower()
        if subcommand == "create":
            if len(args) > 3:
                raise PluginError("Usage: plugin create [name] [kind] [category]")
            if not args:
                if self.session is None:
                    raise PluginError("Use 'plugin create name' in noninteractive mode")
                name = self.session.prompt("Plugin name: ").strip()
                kind = self.session.prompt("Kind [auxiliary]: ").strip() or "auxiliary"
                category = self.session.prompt("Category [custom]: ").strip() or "custom"
                author = self.session.prompt("Author [Community]: ").strip() or "Community"
                description = self.session.prompt("Description [Custom Labsecurity plugin]: ").strip() or "Custom Labsecurity plugin"
            else:
                author, description = "Community", "Custom Labsecurity plugin"
                name = args[0]
                kind = args[1] if len(args) >= 2 else "auxiliary"
                category = args[2] if len(args) >= 3 else "custom"
            path = create_plugin(self.registry.plugin_root, name, kind, category, author, description)
        elif subcommand == "import":
            if not 1 <= len(args) <= 2:
                raise PluginError("Usage: plugin import PATH.py [name]")
            path = import_script(self.registry.plugin_root, Path(args[0]), args[1] if len(args) == 2 else None)
        else:
            if len(args) != 1:
                raise PluginError("Usage: plugin install FOLDER")
            path = install_plugin(self.registry.plugin_root, Path(args[0]))
        self._reload(quiet=True)
        self.output.success(f"Plugin {'installed' if subcommand == 'install' else 'scaffold generated'}: {path.relative_to(self.root)}")
        if subcommand != "install":
            self.output.info("Edit plugin.py and manifest.json, then run 'reload'.")
        self.output.warning("Only run plugins or imported scripts from developers you trust.")

    def _reload(self, quiet: bool = False) -> None:
        for module in self.registry.modules.values():
            self.executor.forget(module)
        active_id = self.selected.id if self.selected else None
        self.registry.refresh()
        self.selected = self.registry.modules.get(active_id) if active_id else None
        # Preserve values for unchanged options only, resetting removed or changed types.
        updated: dict[str, dict[str, Any]] = {}
        for module in self.registry.modules.values():
            settings = module.defaults()
            for name, opt in module.options.items():
                old = self.settings.get(module.id, {}).get(name)
                if old is not None:
                    try:
                        settings[name] = opt.convert(old)
                    except PluginError:
                        pass
            updated[module.id] = settings
        self.settings = updated
        self.last_search = []
        if not quiet:
            self.output.success(f"Reloaded {len(self.registry.modules)} plugins and "
                                f"{len(self.registry.commands)} extension commands")
        for error in self.registry.errors:
            self.output.warning(error)

    def _require_selected(self) -> Plugin:
        if self.selected is None:
            raise PluginError("No module selected. Use 'search' and 'use <module>'.")
        return self.selected

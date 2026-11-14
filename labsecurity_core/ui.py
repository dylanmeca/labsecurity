"""Metasploit-style terminal presentation, independent from the plugin system."""
from __future__ import annotations

from collections import Counter
from rich.console import Console
from rich.table import Table
from rich.text import Text

MASK = r'''
             .-"""""""""-.
           .'  _        _  '.
          /   /_\      /_\   \
         |    \_/  /\  \_/    |
         |         \/         |
         |    \  .----.  /    |
         |     \/ .--. \/     |
         |      \_\__/ _/     |
          \     /  \/  \     /
           '._  \____/  _.'
              '--------'
'''


class Output:
    def __init__(self, console: Console | None = None):
        self.console = console or Console(highlight=False)

    def text(self, message: str = "") -> None:
        self.console.print(message, markup=False, highlight=False)

    def line(self, prefix: str, color: str, message: str) -> None:
        self.console.print(Text.assemble((prefix, f"bold {color}"), (f" {message}", "white")))

    def info(self, message: str) -> None:
        self.line("[*]", "bright_blue", message)

    def success(self, message: str) -> None:
        self.line("[+]", "green", message)

    def warning(self, message: str) -> None:
        self.line("[!]", "yellow", message)

    def error(self, message: str) -> None:
        self.line("[-]", "bright_red", message)

    def banner(self, registry) -> None:
        c = self.console
        c.print(Text(MASK, style="bold red"))
        c.print(Text("                  LABSECURITY", style="bold cyan"))
        c.print()
        c.print(Text("       =[ Labsecurity Framework v2.0.0 ]", style="bold white"))
        stats = Counter(p.kind for p in registry.modules.values())
        # The count reflects successfully discovered plugins, never hardcoded.
        for group in ("auxiliary", "exploit", "post", "custom"):
            count = stats.pop(group, 0)
            c.print(Text.assemble(("+ -- --=[ ", "dim white"),
                                  (str(count), "bold green"),
                                  (f" {group} modules", "white"),
                                  (" ]", "dim white")))
        for group, count in sorted(stats.items()):
            c.print(Text.assemble(("+ -- --=[ ", "dim white"), (str(count), "bold green"),
                                  (f" {group} modules ]", "white")))
        c.print()
        c.print(Text.assemble(("Repository: ", "bold blue"),
                              ("https://github.com/dylanmeca/labsecurity", "underline cyan")))
        c.print(Text("Type 'help' for available commands.\n", style="dim white"))

    def module_table(self, modules: list, title: str = "Matching Modules") -> None:
        c = self.console
        c.print(f"\n{title}", style="bold white")
        c.print("=" * len(title), style="white")
        table = Table(box=None, show_header=True, header_style="bold white", pad_edge=False)
        table.add_column("#", style="dim white", width=4)
        table.add_column("Name", style="cyan", min_width=25)
        table.add_column("Description", style="white")
        for index, module in enumerate(modules):
            table.add_row(str(index), module.id, module.description)
        c.print(table)
        c.print()

    def options_table(self, plugin, values: dict) -> None:
        c = self.console
        title = f"Module options ({plugin.id}):"
        c.print(f"\n{title}\n", style="bold white")
        table = Table(box=None, pad_edge=False, header_style="bold white")
        table.add_column("Name", style="cyan", min_width=13)
        table.add_column("Current Setting", style="yellow", min_width=17)
        table.add_column("Required", style="white", min_width=9)
        table.add_column("Description", style="white")
        for name, option in plugin.options.items():
            value = values.get(name)
            table.add_row(name, "" if value is None else str(value),
                          "yes" if option.required else "no", option.description)
        c.print(table)
        c.print()

"""Labsecurity: extensible, Metasploit-inspired interactive security console.

Run with: python labsecurity.py
No command-line target/script arguments: plugins are managed inside the console.
"""
from pathlib import Path
from labsecurity_core.console import LabsecurityConsole


def main() -> None:
    app = LabsecurityConsole(root=Path(__file__).resolve().parent)
    app.cmdloop()


if __name__ == "__main__":
    main()

"""Demonstrates plugin command extensions without modifying the core."""
import platform
import sys


def run(ctx):
    ctx.success(f"Python {platform.python_version()}")
    ctx.info(f"Operating system: {platform.system()} {platform.release()}")
    ctx.info(f"Interpreter: {sys.executable}")


def doctor(ctx, args):
    ctx.success(f"Python runtime: {sys.version.split()[0]}")
    ctx.info(f"Platform: {platform.platform()}")
    ctx.info("The plugin system is available and this command was loaded from a manifest.")

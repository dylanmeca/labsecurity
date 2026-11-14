"""HTTP response header inspection."""
import requests


def run(ctx):
    address = ctx.get("URL")
    timeout = ctx.get("TIMEOUT")
    if not 1 <= timeout <= 30:
        raise ValueError("TIMEOUT must be between 1 and 30")
    response = requests.get(address, timeout=timeout, headers={"User-Agent": "Labsecurity/2.0"}, stream=True)
    try:
        ctx.info(f"HTTP {response.status_code} - {response.url}")
        for key, value in sorted(response.headers.items(), key=lambda item: item[0].lower()):
            ctx.print(f"  {key}: {value}")
    finally:
        response.close()

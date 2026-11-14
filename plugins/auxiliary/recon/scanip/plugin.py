"""IP metadata using a third-party service. The IP is sent to ipinfo.io."""
import ipaddress
import requests


def run(ctx):
    address = ctx.get("IP")
    ipaddress.ip_address(address)  # Do not forward arbitrary paths to an external API.
    response = requests.get(f"https://ipinfo.io/{address}/json", timeout=ctx.get("TIMEOUT"))
    response.raise_for_status()
    data = response.json()
    if not isinstance(data, dict):
        raise ValueError("Invalid API response")
    if data.get("bogon"):
        ctx.warning("IP is non-public / reserved (bogon)")
    for key, value in data.items():
        ctx.print(f"  {key}: {value}")

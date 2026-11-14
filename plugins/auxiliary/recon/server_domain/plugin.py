"""Reverse IP lookup. Third-party page structure may change without notice."""
import ipaddress
import requests
from bs4 import BeautifulSoup


def run(ctx):
    addr = ctx.get("IP")
    ipaddress.ip_address(addr)
    ctx.warning("This query sends the IP to viewdns.info and may be rate-limited")
    response = requests.get("https://viewdns.info/reverseip/", params={"host": addr, "t": "1"},
                            timeout=ctx.get("TIMEOUT"), headers={"User-Agent": "Labsecurity/2.0"})
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.select_one('table[border="1"]')
    if table is None:
        ctx.warning("No reverse-IP results table found (service markup may have changed)")
        return
    count = 0
    for row in table.select("tr"):
        cells = row.select("td")
        if not cells:
            continue
        text = cells[0].get_text(" ", strip=True)
        if text and text.lower() not in {"domain", "domain name"}:
            ctx.success(text)
            count += 1
    ctx.info(f"Displayed {count} candidate domains; this is not a verified ownership list")

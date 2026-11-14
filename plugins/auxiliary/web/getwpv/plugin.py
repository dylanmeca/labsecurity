"""Read generator metadata; this cannot reliably detect all WordPress installations."""
import requests
from bs4 import BeautifulSoup


def run(ctx):
    response = requests.get(ctx.get("URL"), timeout=ctx.get("TIMEOUT"),
                            headers={"User-Agent": "Labsecurity/2.0"})
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    generators = [tag.get("content", "") for tag in soup.find_all("meta")
                  if tag.get("name", "").lower() == "generator"]
    if generators:
        for item in generators:
            ctx.success(f"Generator: {item}")
    else:
        ctx.warning("No generator meta tag found; WordPress may hide this information")

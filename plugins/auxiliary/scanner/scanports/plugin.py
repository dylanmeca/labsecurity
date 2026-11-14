"""TCP connect scanning; requires authorization from the target owner."""
from concurrent.futures import ThreadPoolExecutor, as_completed
import socket


def _ports(text):
    result = set()
    for section in text.split(","):
        section = section.strip()
        if not section:
            raise ValueError("Empty segment in PORTS")
        if "-" in section:
            first, last = section.split("-", 1)
            first, last = int(first), int(last)
            if first > last:
                raise ValueError("PORTS range start must not exceed the end")
            if first < 1 or last > 65535 or (last - first + 1) > 2048:
                raise ValueError("PORTS must be 1-65535; maximum 2048 ports per scan")
            result.update(range(first, last + 1))
        else:
            result.add(int(section))
        if len(result) > 2048:
            raise ValueError("A single scan is limited to 2048 ports")
    if not result or min(result) < 1 or max(result) > 65535:
        raise ValueError("Valid PORTS values are between 1 and 65535")
    return sorted(result)


def _probe(host, port, timeout):
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return port
    except (socket.timeout, TimeoutError, OSError):
        return None


def run(ctx):
    host = ctx.get("RHOSTS")
    ports = _ports(ctx.get("PORTS"))
    timeout = ctx.get("TIMEOUT")
    workers = ctx.get("THREADS")
    if timeout < 1 or timeout > 30 or workers < 1 or workers > 64:
        raise ValueError("TIMEOUT must be 1-30 seconds and THREADS must be 1-64")
    ctx.info(f"Checking {len(ports)} TCP ports on {host} with {workers} workers")
    open_ports = []
    with ThreadPoolExecutor(max_workers=workers) as pool:
        pending = [pool.submit(_probe, host, port, timeout) for port in ports]
        for result in as_completed(pending):
            found = result.result()
            if found is not None:
                open_ports.append(found)
    for port in sorted(open_ports):
        ctx.success(f"{host}:{port} - TCP open")
    ctx.info(f"Scan finished: {len(open_ports)} open out of {len(ports)} checked")

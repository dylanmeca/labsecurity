"""Port scan using TCP connect, or Nmap when requested."""
import socket


def run(ctx):
    target = ctx.get("RHOSTS")
    port = ctx.get("RPORT")
    timeout = ctx.get("TIMEOUT")
    if timeout < 1 or timeout > 30:
        raise ValueError("TIMEOUT must be between 1 and 30 seconds")
    backend = ctx.get("BACKEND")
    if backend == "nmap":
        try:
            import nmap
        except ImportError as exc:
            raise RuntimeError("Nmap mode needs pip install python-nmap and the nmap executable") from exc
        scanner = nmap.PortScanner()
        scanner.scan(hosts=target, ports=str(port), arguments="-sT -sV --version-intensity 3 -Pn -n")
        for host in scanner.all_hosts():
            tcp = scanner[host].get("tcp", {})
            info = tcp.get(port, {})
            state = info.get("state", "unknown")
            description = " ".join(str(info.get(k, "")) for k in ("name", "product", "version")).strip()
            ctx.success(f"{host}:{port} TCP {state} {description}") if state == "open" else ctx.info(f"{host}:{port} TCP {state}")
    else:
        try:
            with socket.create_connection((target, port), timeout=timeout):
                ctx.success(f"{target}:{port} - TCP port open")
        except (socket.timeout, TimeoutError, OSError) as exc:
            ctx.warning(f"{target}:{port} - connection not established ({exc})")

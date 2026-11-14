"""DNS record lookup using dnspython."""
import dns.resolver


def run(ctx):
    hostname = ctx.get("DOMAIN")
    record_types = [item.strip().upper() for item in ctx.get("TYPES").split(",") if item.strip()]
    if len(record_types) > 12:
        raise ValueError("Maximum 12 DNS record types")
    resolver = dns.resolver.Resolver()
    resolver.lifetime = ctx.get("TIMEOUT")
    for kind in record_types:
        try:
            answers = resolver.resolve(hostname, kind)
            for answer in answers:
                ctx.success(f"{kind:<5} {answer}")
        except dns.resolver.NXDOMAIN:
            ctx.error("Domain does not exist")
            break
        except (dns.resolver.NoAnswer, dns.resolver.NoNameservers, dns.exception.Timeout):
            ctx.warning(f"No {kind} answer from the DNS resolver")

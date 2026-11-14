"""Query NS records for the provided domain."""
import dns.resolver


def run(ctx):
    resolver = dns.resolver.Resolver()
    resolver.lifetime = ctx.get("TIMEOUT")
    answers = resolver.resolve(ctx.get("DOMAIN"), "NS")
    for item in answers:
        ctx.success(f"NS {item}")

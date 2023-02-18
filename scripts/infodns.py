import argparse
import dns.resolver
from colorama import init, Fore, Style

init(autoreset=True)

def run(target):
    print(Style.BRIGHT + Fore.BLUE + "[*] Consulting...")
    information = ['A','AAAA','NS','SOA','MX','MF','MD','TXT']
    for c in information:
        try:
            a = dns.resolver.query(target, c)
            for q in a:
                print(q)
        except:
                print(Style.BRIGHT + Fore.RED + "[*] Could not get query")

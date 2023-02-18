import argparse
import dns.resolver
from colorama import init, Fore, Style

init(autoreset=True)

def run(target):
    try:
        print(Style.BRIGHT + Fore.BLUE + "[*] Scanning NS from DNS...")
        target = dns.resolver.resolve(target, "NS")
        for x in target:
            print(x)

        print(Style.BRIGHT + Fore.BLUE + "[*] Scan finished")
    except:
        print(Style.BRIGHT + Fore.RED + "[*] Error, could not connect to server")

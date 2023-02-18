import argparse
import requests
from colorama import init, Fore, Style

init(autoreset=True)

def run(target):
    try:
        print(Style.BRIGHT + Fore.BLUE + "[*] Scanning website...")
        target = requests.get(url=target)
        header = dict(target.headers)
        for x in header:
            print(x + " : "+header[x])
        print(Style.BRIGHT + Fore.BLUE + "[*] Scan finished")
    except:
        print(Style.BRIGHT + Fore.RED + "[*] Error, could not connect to server")

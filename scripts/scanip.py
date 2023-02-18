import argparse
import json
import urllib.request
from colorama import init, Fore, Style

init(autoreset=True)

def run(target):
    print(Style.BRIGHT + Fore.BLUE + "[*] Scanning ip...")
    url = 'https://ipinfo.io/'+target+'/json'
    openurl = urllib.request.urlopen(url)
    loadurl = json.load(openurl)

    for i in loadurl:
        print(i + " : " + loadurl[i])

    print(Style.BRIGHT + Fore.BLUE + "[*] Scan finished")


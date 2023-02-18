import argparse
import requests
from bs4 import BeautifulSoup
from colorama import init, Fore, Style

init(autoreset=True)

def run(target):
    try:
        print(Style.BRIGHT + Fore.BLUE + "[*] Getting wp version...")
        header = {'User-Agent': 'Firefox'}
        petition = requests.get(url=target, headers=header)
        soup = BeautifulSoup(petition.text, 'html5lib')
        for v in soup.find_all('meta'):
            if v.get('name') == 'generator':
                version = v.get('content')

        print(version)
        print(Style.BRIGHT + Fore.BLUE + "[*] Scan finished")
    except:
        print(Style.BRIGHT + Fore.RED + "[*] Error, could not get wp version")


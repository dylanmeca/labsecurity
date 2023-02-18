import argparse
import nmap
from colorama import init, Fore, Style

init(autoreset=True)

def run(target, port):
    print(Style.BRIGHT + Fore.BLUE + "[*] Scanning port...")
    nm = nmap.PortScanner()
    nm.scan(target, port, arguments='-sV --version-intensity 3')
    print(f"Protocols used: {nm[target].all_protocols()}")
    print(f"Machine status: {nm[target].state()}")

    for ports in nm[target]['tcp'].keys():
        for data in nm[target]['tcp'][ports]:
            print(data + " : " + nm[target]['tcp'][ports][data])

    print(Style.BRIGHT + Fore.BLUE + "[*] Scan finished")

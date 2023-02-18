import argparse
import nmap
from colorama import init, Fore, Style

init(autoreset=True)

def run(target):
    print(Style.BRIGHT + Fore.BLUE + "[*] Scanning ports...")
    nm = nmap.PortScanner()
    ports_open = "-p "
    results = nm.scan(target, arguments="--top-ports 1000 -sT -n -Pn -T4")
    count = 0
    #print (results)
    print(f"\nHost : {target}")
    print(f"State : {nm[target].state()}")
    for proto in nm[target].all_protocols():
        print("Protocol : {}".format(proto))
        lport = nm[target][proto].keys()
        sorted(lport)
        for port in lport:
            print("port : {}\tstate : {}".format(
                port, nm[target][proto][port]["state"]))
            if count == 0:
                ports_open = ports_open+str(port)
                count = 1
            else:
                ports_open = ports_open+","+str(port)

    print(Style.BRIGHT + Fore.BLUE + "\n[*] Ports Open: " + ports_open + " " + "Host: "+str(target))
    print(Style.BRIGHT + Fore.BLUE + "[*] Scan finished")

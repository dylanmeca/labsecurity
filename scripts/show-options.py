from colorama import init, Fore, Style

init(autoreset=True)

def run():
    print(Style.BRIGHT + Fore.BLUE + "[*] Command example: python3 labsecurity -t 192.168.0.107 -p 80 scanport.py")
    print(Style.BRIGHT + Fore.BLUE + "[*] Script List: ")
    print("scanweb.py => Gets the information from the headers of a website")
    print("scanports.py => Scan all the ports of an IP")
    print("scanport.py => Scan the port of an ip")
    print("scanip.py => Geolocate an ip")
    print("scanns.py => Get authorization name server")
    print("getwpv.py => Get the WordPress version")
    print("infodns.py => Show DNS information")
    print("server-domain.py => Detects domains hosted on a server")

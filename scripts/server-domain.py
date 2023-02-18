import requests
from bs4 import BeautifulSoup
from colorama import init, Fore, Style

init(autoreset=True)

def run(target):
    print(Style.BRIGHT + Fore.BLUE + "[*] Consulting...")
    agent = {'User-Agent':'Firefox'}
    a = requests.get("https://viewdns.info/reverseip/?host={}&t=1".format(target),headers=agent)
    b = BeautifulSoup(a.text,'html5lib')
    c = b.find(id="null")
    d = c.find(border="1")
    for l in d.find_all("tr"):
        print(Style.BRIGHT + Fore.BLUE + "[*] Domain hosted on the server: " + l.td.string)

import os, sys, time, urllib.request, requests
from colorama import init, Fore
from labtool.headers import *

init(autoreset=True)

def terminal ():

         while True:
            
               user = input (">>> ")
               prompt = user.split ()

               if not prompt:
                      print (Fore.RED + "[*] ERROR")
               elif prompt[0] == 'help':
                      print (Fore.CYAN + "set ip => register the ip in the system")
               elif prompt[0] == 'set':
                      if prompt[1] == 'ip':
                             global ip1
                             print (Fore.GREEN + "ip =>", prompt[2])
                             ip1 = prompt[2]
               elif prompt[0] == 'exit' or prompt[0] == 'quit':
                      break
               elif prompt[0] == 'run' or prompt[0] == 'exploit':
                      if ip1 == ip1:
                             target = requests.get(url=ip1)
                             header = dict(target.headers)
                             for x in header:
                                 print (x+ " : "+header[x])
               else:
                    print (Fore.RED + "[*] ERROR")

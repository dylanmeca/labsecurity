import os, sys, time, urllib.request, requests
from colorama import init, Fore
from labtool.main import *
from labtool.scanners import *

init(autoreset=True)

scanner = scanner ()

main = main ()

def terminal ():
         
         while True:
               
               try:
                   user = input ("lab-tool > ")
                   prompt = user.split ()

                   if not prompt:
                         print (Fore.RED + "[*] ERROR")
                   elif prompt[0] == 'help':
                         main.help ()
                   elif prompt[0] == 'set':
                         if prompt[1] == 'ip':
                               global ip1
                               print (Fore.GREEN + "ip =>", prompt[2])
                               ip1 = prompt[2]
                         if prompt[1] == 'port':
                               global port1
                               print (Fore.GREEN + "port =>", prompt[2])
                               port1 = prompt[2]
                   elif prompt[0] == 'use':
                         global use1
                         if prompt[1] == 'scanweb':
                               print (Fore.GREEN + "use =>", prompt[1])
                               use1 = prompt[1]
                         if prompt[1] == 'scanports':
                               print (Fore.GREEN + "use =>", prompt[1])
                               use1 = prompt[1]
                         if prompt[1] == 'scanport':
                               print (Fore.GREEN + "use =>", prompt[1])
                               use1 = prompt[1]
                         if prompt[1] == 'scanip':
                               print (Fore.GREEN + "use =>", prompt[1])
                               use1 = prompt[1]
                   elif prompt[0] == 'exit' or prompt[0] == 'quit':
                         break
                   elif prompt[0] == 'run' or prompt[0] == 'exploit':
                         if use1 == 'scanweb':
                             scanner.scanweb (ip1)
                         if use1 == 'scanports':
                             scanner.scanports(ip1)
                         if use1 == 'scanport':
                             scanner.scanport (ip1, port1)
                         if use1 == 'scanip':
                             scanner.scanip (ip1)
                   else:
                         print (Fore.RED + "[*] ERROR")

               except ValueError:
                        print (Fore.GREEN + "Error, there is a type of error.")
                        sys.exit ()
               except KeyboardInterrupt:
                        print (Fore.GREEN + "Exiting...")
                        sys.exit ()
               except NameError:
                        print (Fore.GREEN + "Error, the command I use is not available in the program code.")
                        sys.exit ()
               except SyntaxError:
                        print (Fore.GREEN + "Error, the code has a syntax error.")
                        sys.exit ()
               except TypeError:
                        print (Fore.GREEN + "Error, the code is misspelled.")
                        sys.exit ()

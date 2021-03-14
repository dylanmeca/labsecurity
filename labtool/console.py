import os, sys, time, urllib.request, requests
from colorama import init, Fore
from labtool.headers import *
from labtool.main import *
from labtool.scanners import *

init(autoreset=True)

scanner = scanner ()

header = header ()

logo ()

def terminal ():
         
         while True:
               
               try:
                   user = input ("lab-tool > ")
                   prompt = user.split ()

                   if not prompt:
                         print (Fore.RED + "[*] ERROR")
                   elif prompt[0] == 'help':
                         print (Fore.CYAN + "set ip => register the ip in the system")
                         print (Fore.CYAN + "use headerweb => Use a script that extracts information from a website")
                         print (Fore.CYAN + "run or exploit => The run and exploit command is to start the system")
                         print (Fore.CYAN + "exit or quit => Is to exit the system ")
                   elif prompt[0] == 'set':
                         if prompt[1] == 'ip':
                               global ip1
                               print (Fore.GREEN + "ip =>", prompt[2])
                               ip1 = prompt[2]
                   elif prompt[0] == 'use':
                         if prompt[1] == 'headerweb':
                               global use1
                               print (Fore.GREEN + "use =>", prompt[1])
                               use1 = prompt[1]
                         if prompt[1] == 'scanports':
                               global use1
                               print (Fore.GREEN + "use =>", prompt[1])
                               use1 = prompt[1]
                   elif prompt[0] == 'exit' or prompt[0] == 'quit':
                         break
                   elif prompt[0] == 'run' or prompt[0] == 'exploit':
                         if use1 == 'headerweb':
                             header.headerweb (ip1)
                         if use1 == 'scanports':
                             scanner.scanports(ip1)
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

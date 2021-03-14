import os, sys, time, urllib.request, requests
from colorama import init, Fore
from labtool.headers import *

init(autoreset=True)

def terminal ():

         while True:
               
               try:
                   user = input ("lab-tool > ")
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
                             header = header ()
                             header.headerweb (ip1)
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

import os, sys, time, urllib.request, requests
from colorama import init, Fore, Style
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
                         print (Style.BRIGHT + Fore.RED + "[*] ERROR, you must add a command")
                   elif prompt[0] == 'help':
                         main.help ()
                   elif prompt[0] == 'set':
                         if prompt[1] == 'ip':
                               global ip1
                               print (Style.BRIGHT + Fore.GREEN + "ip =>", prompt[2])
                               ip1 = prompt[2]
                         if prompt[1] == 'port':
                               global port1
                               print (Style.BRIGHT + Fore.GREEN + "port =>", prompt[2])
                               port1 = prompt[2]
                   elif prompt[0] == 'use':
                         global use1
                         if prompt[1] == 'scanweb':
                               print (Style.BRIGHT + Fore.GREEN + "use =>", prompt[1])
                               use1 = prompt[1]
                         if prompt[1] == 'scanports':
                               print (Style.BRIGHT + Fore.GREEN + "use =>", prompt [1])
                               use1 = prompt[1]
                         if prompt[1] == 'scanport':
                               print (Style.BRIGHT + Fore.GREEN + "use =>", prompt[1])
                               use1 = prompt[1]
                         if prompt[1] == 'scanip':
                               print (Style.BRIGHT + Fore.GREEN + "use =>", prompt[1])
                               use1 = prompt[1]
                   elif prompt[0] == 'exit' or prompt[0] == 'quit':
                         break
                   elif prompt[0] == 'run' or prompt[0] == 'exploit':
                         if use1 == 'scanweb':
                             print (Style.BRIGHT  + Fore.BLUE + "[*] Scanning website...")
                             scanner.scanweb (ip1)
                         if use1 == 'scanports':
                             print (Style.BRIGHT + Fore.BLUE + "[*] Scanning ports...")
                             scanner.scanports(ip1)
                         if use1 == 'scanport':
                             print (Style.BRIGHT + Fore.BLUE + "[*] Scanning port...")
                             scanner.scanport (ip1, port1)
                         if use1 == 'scanip':
                             print (Style.BRIGHT + Fore.BLUE + "[*] Scanning ip...")
                             scanner.scanip (ip1)
                   else:
                         print (Style.BRIGHT + Fore.RED + "[*] ERROR, use the help command for more information")

               except ValueError:
                        print (Style.BRIGHT + Fore.RED + "[*] Error, there is a type of error.")
                        sys.exit ()
               except KeyboardInterrupt:
                        print (Style.BRIGHT + Fore.BLUE + "[*] Exiting...")
                        sys.exit ()
               except NameError:
                        print (Style.BRIGHT + Fore.RED + "[*] Error, the command I use is not available in the program code.")
                        sys.exit ()
               except SyntaxError:
                        print (Style.BRIGHT + Fore.RED + "[*] Error, the code has a syntax error.")
                        sys.exit ()
               except TypeError:
                        print (Style.BRIGHT + Fore.RED + "[*] Error, the code is misspelled.")
                        sys.exit ()
               except IndexError:
                        print (Style.BRIGHT + Fore.RED + "[*] ERROR, the command is incomplete or there is a fault, please use the help command") 
               except KeyError:
                        print (Style.BRIGHT + Fore.RED + "[*] ERROR, ha chose the wrong argument - KeyError: {}".format (prompt [1]))                 

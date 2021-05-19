import platform
from colorama import init, Fore, Style

init(autoreset=True)

class interpreter:

      def __init__(self):
             #print ("Hello World")
             return

      def help (self):
             print (Style.BRIGHT + Fore.GREEN + "set target => register the target in the system")
             print (Style.BRIGHT + Fore.GREEN + "use scanweb => Use a script that extracts information from a website")
             print (Style.BRIGHT + Fore.GREEN + "run or exploit => The run and exploit command is to start the system")
             print (Style.BRIGHT + Fore.GREEN + "exit or quit => Is to exit the system ")
             print (Style.BRIGHT + Fore.GREEN + "use scanports => Scan all the ports of an IP")
             print (Style.BRIGHT + Fore.GREEN + "use scanport => Scan the port of an ip")
             print (Style.BRIGHT + Fore.GREEN + "set port => register the port in the system")
             print (Style.BRIGHT + Fore.GREEN + "use scanip => Geolocate an ip")

      def command_ls (self):
             system = platform.system()
             if system == 'Windows':
                    return 'dir'
             elif system == 'Linux':
                    return 'ls'
             else:
                    return

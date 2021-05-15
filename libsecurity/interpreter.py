import os
import sys
import time
from .main import *
from .core.scanners import *
from colorama import init, Fore, Style

init(autoreset=True)

class process:

      def __init__(self):
            return

      def command_help (self, data):
            self.data = data
            main.help (self.data)

      def command_set (self, data):
            #Here is the part where the selections are put
            self.data = data
            self.prompt = data.split ()
            
            if self.prompt[1] == 'ip':
                 print (Style.BRIGHT + Fore.GREEN + "ip =>", self.prompt[2])
                 ip = self.prompt[2]
                 self.ip = ip
            elif self.prompt[1] == 'port':
                 print (Style.BRIGHT + Fore.GREEN + "port =>", self.prompt[2])
                 port = self.prompt[2]
                 self.port = port
            else:
                 print (Style.BRIGHT + Fore.RED + "[*] Error, the command is misspelled")

      def command_use (self, data):
            #Here is the part where one of the following categories is used
            self.data = data
            self.prompt = data.split ()
            if self.prompt[1] == 'scanweb':
               print (Style.BRIGHT + Fore.GREEN + "use =>", self.prompt[1])
               self.use = self.prompt[1]
            elif self.prompt[1] == 'scanports':
               print (Style.BRIGHT + Fore.GREEN + "use =>", self.prompt[1])
               self.use = self.prompt[1]
            elif self.prompt[1] == 'scanport':
               print (Style.BRIGHT + Fore.GREEN + "use =>", self.prompt[1])
               self.use = prompt[1]
            elif self.prompt[1] == 'scanip':
               print (Style.BRIGHT + Fore.GREEN + "use =>", self.prompt[1])
               self.use = self.prompt[1]
            else:
                print (Style.BRIGHT + Fore.RED + "[*] Error, the command is misspelled")

      def command_clear (self, data):
            self.data = data
            os.system (data)

      def command_exit (self):
            sys.exit ()

      def command_run (self):
            if self.use == 'scanweb':
                print (Style.BRIGHT  + Fore.BLUE + "[*] Scanning website...")
                scanner.scanweb (self.ip)
            elif self.use == 'scanports':
                print (Style.BRIGHT + Fore.BLUE + "[*] Scanning ports...")
                scanner.scanports(self.ip)
            elif self.use == 'scanport':
                print (Style.BRIGHT + Fore.BLUE + "[*] Scanning port...")
                scanner.scanport (self.ip, self.port)
            elif self.use == 'scanip':
                print (Style.BRIGHT + Fore.BLUE + "[*] Scanning ip...")
                scanner.scanip (self.ip)
            else:
                print (Style.BRIGHT + Fore.RED + "[*] Error, the command is misspelled")



                 
                               

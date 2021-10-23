import platform
from colorama import init, Fore, Style

init(autoreset=True)


class interpreter:

    def __init__(self):
        #print ("Hello World")
        return

    def help(self):
        print(Style.BRIGHT + Fore.GREEN + """
        show options => Show system options
        exit or quit => Is to exit the system 
        """)

    def command_ls(self):
        system = platform.system()
        if system == 'Windows':
            return 'dir'
        elif system == 'Linux':
            return 'ls'
        else:
            return

    def command_clear(self):
        system = platform.system()
        if system == 'Windows':
            return 'cls'
        elif system == 'Linux':
            return 'clear'
        else:
            return

    def show_options(self):
          print(Style.BRIGHT + Fore.GREEN + """
          set target => register the target in the system
          use scanweb => Use a script that extracts information from a website
          run or exploit => The run and exploit command is to start the system
          use scanports => Scan all the ports of an IP
          use scanport => Scan the port of an ip
          set port => register the port in the system
          use scanip => Geolocate an ip
          scanns => Get authorization name server
          use getwpv => Get the WordPress version
          """)

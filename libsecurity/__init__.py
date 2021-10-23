from libsecurity.scanners import *
from libsecurity.main import *

scanner = scanner()
interpreter = interpreter()

scanports = scanner.scanports
scanport = scanner.scanport
scanip = scanner.scanip
scanweb = scanner.scanweb
scanns = scanner.scanns
getwpv = scanner.getwpv

help = interpreter.help
command_ls = interpreter.command_ls
show_options = interpreter.show_options
command_clear = interpreter.command_clear

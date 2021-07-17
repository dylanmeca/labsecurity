from libsecurity.scanners import *
from libsecurity.main import *

scanner = scanner()
interpreter = interpreter()

scanports = scanner.scanports
scanport = scanner.scanport
scanip = scanner.scanip
scanweb = scanner.scanweb
scanns = scanner.scanns

help = interpreter.help
command_ls = interpreter.command_ls

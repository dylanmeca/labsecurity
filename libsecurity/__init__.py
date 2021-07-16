from libsecurity.scanners import *
from libsecurity.main import *

scanner = scanner()
interpreter = interpreter()

scanports = scanner.scanports
scanport = scanner.scanport
scanip = scanner.scanip
scanweb = scanner.scanweb

help = interpreter.help
command_ls = interpreter.command_ls
myip = interpreter.myip

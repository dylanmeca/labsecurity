import os, sys, time, nmap

class scanner:

        def ___init__(self):
                #print ("Welcome")
                return

        def scanports(self,ip):
                self.ip = ip
                nm = nmap.PortScanner()
                nm.scan(hosts=ip, arguments="--top-ports 1000 -sV --version-intensity 3")
                print ("Command executed: {}".format(nm.command_line())



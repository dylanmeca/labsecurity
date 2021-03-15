import os, sys, time, nmap

class scanner:

        def ___init__(self):
                #print ("Welcome")
                return

        def scanports(self,ip):
                self.ip = ip
                nm = nmap.PortScanner()
                nm.scan(ip, arguments='--top-ports 1000 -sV --version-intensity 3')
                print ("Command executed: {}".format(nm.command_line()))
                print ("Protocols used: {}".format(nm[ip].all_protocols()))
                print ("Machine status: {}".format(nm[ip].state()))

                for ports in nm[ip]['tcp'].keys ():
                     for data in nm[ip]['tcp'][ports]:
                             print (data + " : " + nm[ip]['tcp'][ports][data])



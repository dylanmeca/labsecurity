import os, sys, time, nmap

class scanner:

        def ___init__(self):
                #print ("Welcome")
                return

        def scanports(self,ip,port):
                self.ip = ip
                self.port = port
                nm = nmap.PortScanner()
                nm.scan(ip, port)
                print ("Command executed: {}".format(nm.command_line()))
                print ("Protocols used: {}".format(nm[ip].all_protocols()))
                print ("Machine status: {}".format(nm[ip].state()))

                for ports in nm[ip]['tcp'].keys ():
                     for data in nm[ip]['tcp'][ports]:
                             print (data + " : " + nm[ip]['tcp'][ports][data])



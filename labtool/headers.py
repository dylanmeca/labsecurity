import os, sys, time, requests

class header:

       def __init__(self):
               #print ("Welcome")
               return

       def headerweb (self,link):
               try:
                  self.link = link
                  target = requests.get(url=link)
                  header = dict(target.headers)
                  for x in header:
                       print (x+ " : "+header[x])
               except:
                  print ("[*] Error, could not connect to server")
 

try:
 import usocket as socket        #importing socket
except:
 import socket
import network            #importing network
import esp                 #importing ESP
esp.osdebug(None)
import gc
gc.collect()
ssid = 'ESP_AP'                  #Set your own 
password = '12345678'      #Set your own password


ap = network.WLAN(network.AP_IF)
ap.active(True)            #activating
ap.config(essid=ssid, password=password)

while ap.active() == False:
  pass
print('Connection is successful')
print(ap.ifconfig())

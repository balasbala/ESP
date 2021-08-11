try:
 import usocket as socket        

except:
 import socket

import network            
import esp
from time import sleep
from machine import Pin

esp.osdebug(None)
import gc
gc.collect()


ssid = 'EVERYTHING is'
password = 'Bala@2305'

station = network.WLAN(network.STA_IF)

station.active(True)
station.connect(ssid, password)

#while station.isconnected() == False:
sleep(10)

if station.isconnected() == True:
    print('Station Mode Connection successfull')
    print(station.ifconfig())

    led = Pin(2, Pin.OUT)
    
elif station.isconnected() == False:
    print('AP Mode Connection successfull')
    station.active(False)
    
    ssid = 'ESP_AP'                   
    password = '12345678'
    
    ap = network.WLAN(network.AP_IF)
    ap.active(True)            
    ap.config(essid=ssid, password=password)

    while ap.active() == False:
        pass
    print('Connection is successful')
    print(ap.ifconfig())
    
    
    def web_page():
        html = """<html><head><meta name="viewport" content="width=device-width, initial-scale=1"></head>
        <body><h1>Welcome to "NEEVEE"!</h1></body></html>"""
        return html
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   
    s.bind(('', 80))
    s.listen(5)
    
    while True:
        print("Hello")
        conn, addr = s.accept()
        print('Got a connection from %s' % str(addr))
        request = conn.recv(1024)
        print('Content = %s' % str(request))
        response = web_page()
        conn.send(response)
        conn.close()
          

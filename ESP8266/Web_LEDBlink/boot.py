try:
  import usocket as socket
except:
  import socket

from machine import Pin
import network

import esp
esp.osdebug(None)

import gc
gc.collect()

ssid = 'EVERYTHING is'
password = 'Bala@2305'

station = network.WLAN(network.STA_IF)

station.active(True)
station.connect(ssid, password)

while station.isconnected() == False:
  count = count+1
  if count > 200:
      break

print('Connection successful')
print(station.ifconfig())

led = Pin(2, Pin.OUT)

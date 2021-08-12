# Clean Box Bluetooth Low Energy Firmware Application.
#

#import bluetooth
import random
#import struct
import time
from ble_advertising import advertising_payload
from machine import Pin
from WAVWifi import WAVWireless
import machine
import socket
import usocket as socket
import _thread

'''_IRQ_CENTRAL_CONNECT = const(1)
_IRQ_CENTRAL_DISCONNECT = const(2)
_IRQ_GATTS_WRITE = const(4)

_CLEANBOX_UUID = bluetooth.UUID('FE400000-B5A3-F393-E0A9-E50E24DCCA9E')
_LOCK_CHAR = (bluetooth.UUID('FE400001-B5A3-F393-E0A9-E50E24DCCA9E'), bluetooth.FLAG_WRITE | bluetooth.FLAG_READ,)
_OZONE_CHAR = (bluetooth.UUID('FE400002-B5A3-F393-E0A9-E50E24DCCA9E'), bluetooth.FLAG_WRITE | bluetooth.FLAG_READ,)
_DITIME_CHAR = (bluetooth.UUID('FE400003-B5A3-F393-E0A9-E50E24DCCA9E'), bluetooth.FLAG_WRITE | bluetooth.FLAG_READ,)
_BOXSTAT_CHAR = (bluetooth.UUID('FE400004-B5A3-F393-E0A9-E50E24DCCA9E'), bluetooth.FLAG_NOTIFY,)
_WIFICFG_CHAR = (bluetooth.UUID('FE400005-B5A3-F393-E0A9-E50E24DCCA9E'), bluetooth.FLAG_WRITE | bluetooth.FLAG_READ,)

_CLEANBOX_SERVICE = ( _CLEANBOX_UUID, (_LOCK_CHAR, _OZONE_CHAR, _DITIME_CHAR, _BOXSTAT_CHAR, _WIFICFG_CHAR,), )

SERVICES = ( _CLEANBOX_SERVICE, )

# org.bluetooth.characteristic.gap.appearance.xml
_ADV_APPEARANCE_GENERIC_COMPUTER = const(128)


class CleanBox:
    def __init__(self, ble, name="WAVDisinfect"):
        self._ble = ble
        self.conn_handle = 0
        self.ditime = 0
        self._ble.active(True)
        self._ble.irq(handler=self._irq)
        self.p2 = Pin(2, Pin.OUT, 1)
        self.p2.value(0)
        self.p32 = Pin(32, Pin.OUT, 1)
        self.p32.value(0)
        self._buffer = bytearray()
        self.lock_open = False
        ((self._lock_handle,self._ozone_handle, self.ditime_handle, self.status_handle, self.wificfg_handle,),) = self._ble.gatts_register_services(SERVICES)
        self._connections = set()
        #, appearance=_ADV_APPEARANCE_GENERIC_THERMOMETER
        # , services=[_CLEANBOX_UUID]
        self._payload = advertising_payload(
            name=name, appearance = _ADV_APPEARANCE_GENERIC_COMPUTER
        )
        self._advertise()'''

def _irq(self, event, data):
            with open("wifiap.json", "w") as fp:
                res = str.split(':')
                fdata = "wifiap:"+res[0]+",password:"+res[1]
                print(fdata)
                fp.write(fdata)
                fp.close()
            
            print(res[0])
                #self._ble.gatts_write(self.wificfg_handle, res[0])
                           
    
def wavdisinfect():
    w = WAVWireless()
    w.scanAndConnect()
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
        
    s = socket.socket()
    s.bind(addr)
    s.listen(5)

    print('listening on', addr)
     
    while True:
        conn, addr = s.accept()
        print('Got a connection from %s' % str(addr))
        request = conn.recv(1024)
        request = str(request)
        print('Content = %s' % request)
        sloc = request.find('/?dtime=')
        print(sloc)
        conn.send('HTTP/1.1 200 OK\n')
        conn.send('Content-Type: text/html\n')
        conn.send('Connection: close\n\n')
        conn.sendall("OK")
        conn.close()
        if sloc > 0 and sloc < 50:
            sub = request[sloc:]
            ss = sub.split(' ')
            global dt
            dt = int(ss[0].replace("/?dtime=",""))
            
if __name__ == "__main__":
    wavdisinfect()
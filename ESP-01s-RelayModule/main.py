# Clean Box Bluetooth Low Energy Firmware Application.
#

import random
import struct
import time
from machine import Pin
from micropython import const
from WAVWifi import WAVWireless
import machine
import socket
import usocket as socket

class CleanBox:
    def __init__(self, name="WAVDisinfect"):
        self.conn_handle = 0
        self.ditime = 0
        #self.p2 = Pin(16, Pin.OUT, 1)
        #self.p2.value(0)
        self.p32 = Pin(0, Pin.OUT)
        self.p32.value(1)
        self.lock_open = False

def cleanbox():
    cbox = CleanBox(ble)

    t = 25
    i = 0

    while True:
        time.sleep_ms(1000)
        if cbox.lock_open == True:
            print('lock opened')
            try:
                notify_buf = bytearray(b'\x01\x00')
                cbox._ble.gatts_notify(cbox.conn_handle, cbox.status_handle, notify_buf)
            except Exception:
                print('Exception on notifying the status')
            time.sleep(60)
            print('ozone is activated')
            try:
                notify_buf = bytearray(b'\x01\x01')
                cbox._ble.gatts_notify(cbox.conn_handle, cbox.status_handle, notify_buf)
            except Exception:
                print('Exception on notifying the status')
            cbox.p32.value(0)
            time.sleep(180)
            print('ozone is deactivated')
            cbox.p32.value(1)
            #cbox.p2.value(0)
            cbox.lock_open = False
            print('lock closed')
            try:
                notify_buf = bytearray(b'\x00\x00')
                cbox._ble.gatts_notify(cbox.conn_handle, cbox.status_handle, notify_buf)
            except Exception:
                print('Exception on notifying the status')
        elif cbox.ditime != 0:
            print('ozone is activated')
            cbox.p32.value(0)
            try:
                notify_buf = bytearray(b'\x00\x01')
                cbox._ble.gatts_notify(cbox.conn_handle, cbox.status_handle, notify_buf)
            except Exception:
                print('Exception on notifying the status')
            ditime = 0
            while ditime < (60 * cbox.ditime):
                time.sleep(1)
                ditime = ditime + 1
            cbox.p32.value(1)
            cbox.ditime = 0
            print('lock closed')
            try:
                notify_buf = bytearray(b'\x00\x00')
                cbox._ble.gatts_notify(cbox.conn_handle, cbox.status_handle, notify_buf)
            except Exception:
                print('Exception on notifying the status')            

def threadFunction():
    print('ozone is activated')
    global cbox
    cbox.p32.value(0)
    global dt

    ditime = 0
    while ditime < (60 * dt):
        time.sleep(1)
        ditime = ditime + 1
    cbox.p32.value(1)
    cbox.ditime = 0
    print('lock closed')          
    
def wavdisinfect():
    global cbox
    cbox = CleanBox()
    w = WAVWireless()
    
    ret = w.scanAndConnect()
    if ret == False:
        ssid = 'ESP_AP'                   
        password = '12345678'
        global ap
        ap = network.WLAN(network.AP_IF)
        ap.active(True)            
        ap.config(essid=ssid, password=password)

        while ap.active() == False:
          pass
        print('Connection is successful')
        print(ap.ifconfig())

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
        if sloc > 0 and sloc < 50:
            sub = request[sloc:]
            ss = sub.split(' ')
            conn.send('HTTP/1.1 200 OK\n')
            conn.send('Content-Type: text/html\n')
            conn.send('Connection: close\n\n')
            conn.sendall("OK")
            conn.close()
            global dt
            dt = int(ss[0].replace("/?dtime=",""))
            if dt > 0:
                threadFunction()
                #_thread.start_new_thread(threadFunction, ())
            else:
                cbox.p32.value(1)
                dt = 0
        else:
            apidx = request.find('/?wifiap=')
            if apidx > 0:
                sub = request[apidx:]
                ss = sub.split(' ')
                global apname
                data = ss[0].replace("/?wifiap=","")
                fb=open("wifiap.json","w")
                res = data.split(':')
                fdata = "wifiap:"+res[0]+",password:"+res[1]
                fb.write(fdata)
                print("data write",fdata)
                fb.close()
                conn.send('HTTP/1.1 200 OK\n')
                conn.send('Content-Type: text/html\n')
                conn.send('Connection: close\n\n')
                conn.sendall("OK")
                conn.close()
                global ap
                ap.active(False)
                w = WAVWireless()
                ret = w.scanAndConnect()
                if ret == False:
                    print("Error on wifi connection")
                
                
if __name__ == "__main__":
    wavdisinfect()

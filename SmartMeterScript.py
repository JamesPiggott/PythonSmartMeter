#!/usr/bin/env python
# Script to read Smart meters, optionally the data can then be transmitted with a UDP client
# James Piggott @ Universiteit Twente, Netherlands

versie = "1.2"
import sys
import serial
import socket
import time

## Main Program
print ("DSMR P1 reader",  versie)
print ("Press Control-C to stop")

## Set serial port configuration
ser = serial.Serial()
opts = [(9600, serial.SEVENBITS, serial.PARITY_EVEN, serial.STOPBITS_ONE, 1, 0, 8), (115200, serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_ONE, 0, 0, 8)]
ser.port="/dev/ttyUSB0"

## Open COM port
def reconnect():
    global ser
    print ('Trying to open port')
    abort_after = 20
    check = False
    while not check:
        for opt in opts:
            try:
                print ("Probe", opt)
                start = time.time()
                try:
                    ser.close()
                except:
                    pass
                ser.baudrate, ser.bytesize, ser.parity, ser.stopbits, ser.xonxoff, ser.rtscts, ser.timeout = opt
                ser.open()
                ## Check if messages are readible
                while True:
                    p1_raw = ser.readline()
                    delta = time.time() - start
                    if '1-0:1.7.0' in p1_raw:
                        check = True
                        print ("OK, starting listen")
                        break
                    if delta >= abort_after:
                        print ('Moving to other protocol')
                        break
                    time.sleep(0.05)
                if check:
                    break
                else:
                    try:
                        ser.close()
                    except:
                        pass
            except:
                print ("Error with opening:  %s."  % ser.name)
                time.sleep(10)
reconnect()


## Read from the COM port
while True:
    p1_line=''

    try:
        p1_raw = ser.readline()
    except:
        print ("Serial port %s could not be read. " % ser.name)
        time.sleep(20)
        reconnect()
        continue

    try:
        p1_str=str(p1_raw)
        p1_line=p1_str.strip()
    except:
        print "Could not turn P1 line into string"
        time.sleep(5)
        continue

    print (p1_line)

    # Send p1 input over UDP client.
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(p1_line, ("127.0.0.1", 5005))

#Close port and show status
try:
    ser.close()
except:
    sys.exit ("%s. Program stopped. Serial port could not be closed." % ser.name )

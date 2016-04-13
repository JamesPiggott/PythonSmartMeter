#!/usr/bin/env python
# Script to read Smart meters, optionally the data can then be transmitted with a UDP client
# James Piggott @ Universiteit Twente, Netherlands

versie = "1.1"
import sys
import serial
import socket
import time

## Main Program
print ("DSMR P1 reader",  versie)
print ("Press Control-C to stop")

## Set serial port configuration
ser = serial.Serial()
ser.baudrate = 9600
ser.bytesize=serial.SEVENBITS
ser.parity=serial.PARITY_EVEN
ser.stopbits=serial.STOPBITS_ONE
ser.xonxoff=0
ser.rtscts=0
ser.timeout=20
ser.port="/dev/ttyUSB0"

## Open COM port
try:
    ser.open()

    abort_after = 20
    start = time.time()
    check = False

    ## Check if messages are readible
    while True:
        p1_raw = ser.readline()
        delta = time.time() - start
        if delta >= abort_after:
            break
        if '1-0:1.7.0' in p1_raw:
            check = True
            break

    ## Switch to alternative protocol if necessary
    if check == False:
        ser.close()
        ser.baudrate = 115200
        ser.bytesize=serial.EIGHTBITS
        ser.parity=serial.PARITY_EVEN
        ser.stopbits=serial.STOPBITS_ONE
        ser.open()
 
except:
    sys.exit ("Error with opening:  %s."  % ser.name)

## Read from the COM port
while True:
    p1_line=''

    try:
        p1_raw = ser.readline()
            
    except:
        sys.exit ("Serial port %s could not be read. " % ser.name )
    
    p1_str=str(p1_raw)
    p1_line=p1_str.strip()

    print (p1_line)

    # Send p1 input over UDP client.
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(p1_line, ("127.0.0.1", 5005))

#Close port and show status
try:
    ser.close()
except:
    sys.exit ("%s. Program stopped. Serial port could not be closed." % ser.name )

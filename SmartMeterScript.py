#!/usr/bin/env python
# Script to read Smart meters, optionally the data can then be transmitted with a UDP client
# James Piggott @ Universiteit Twente, Netherlands

versie = "1.0"
import sys
import serial
import socket

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

    ### TODO, allow the option to listen to an alternative protocol (for Landis Gyr E350).
 
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
#!/bin/bash

mkfifo /tmp/smartmeter 2>/dev/null

while true; do cu -l /dev/ttyUSB0 -s 9600 --parity=even > /tmp/smartmeter; sleep 5; done

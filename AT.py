#!/usr/bin/env python3

import RPi.GPIO as GPIO
import serial
import time

ser = serial.Serial("/dev/serial0",9600)
ser.flushInput()

power_key = 4
command_input = 'AT'  # Fester AT-Befehl
rec_buff = ''

def power_on(power_key):
    print('GPIO power_key 4 SIM7000X is starting:')
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(power_key,GPIO.OUT)
    time.sleep(0.1)
    GPIO.output(power_key,GPIO.HIGH)
    time.sleep(2)
    GPIO.output(power_key,GPIO.LOW)
    time.sleep(1)
    ser.flushInput()
    print('GPIO power_key 4 SIM7000X is ready')

def power_down(power_key):
    print('GPIO power_key 4 SIM7000X is loging off:')
    GPIO.output(power_key,GPIO.HIGH)
    time.sleep(3)
    GPIO.output(power_key,GPIO.LOW)
    time.sleep(1)
    print('Good bye')

try:
    power_on(power_key)

    # Senden des festen AT-Befehls
    ser.write((command_input + '\r\n').encode())
    time.sleep(0.1)
    if ser.inWaiting():
        time.sleep(0.01)
        rec_buff = ser.read(ser.inWaiting())
    if rec_buff != '':
        print(rec_buff.decode())
        rec_buff = ''

except:
    ser.close()
    power_down(power_key)
    GPIO.cleanup()
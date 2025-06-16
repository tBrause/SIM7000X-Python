#!/usr/bin/python

import RPi.GPIO as GPIO
import serial
import time

ser = serial.Serial('/dev/serial0',9600)
ser.flushInput()

power_key = 6
rec_buff = ''
APN = 'internet'
server_ip = 'linux.sanberlin.com'
Port = '80'

def power_on(power_key):
	print('SIM7000X is starting')
	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)
	GPIO.setup(power_key,GPIO.OUT)
	time.sleep(0.1)
	GPIO.output(power_key,GPIO.HIGH)
	time.sleep(2)
	GPIO.output(power_key,GPIO.LOW)
	time.sleep(2)
	ser.flushInput()
	print('SIM7000X is ready')

def power_down(power_key):
	print('SIM7000X is loging off')
	GPIO.output(power_key,GPIO.HIGH)
	time.sleep(3)
	GPIO.output(power_key,GPIO.LOW)
	time.sleep(2)
	print('Good bye\n')
	
def send_at(command,back,timeout):
	rec_buff = ''
	ser.write((command+'\r\n').encode())
	time.sleep(timeout)
	if ser.inWaiting():
		time.sleep(0.1 )
		rec_buff = ser.read(ser.inWaiting())
	if rec_buff != '':
		if back not in rec_buff.decode():
			print(command + ' ERROR')
			print(command + ' back:\t' + rec_buff.decode())
			return 0
		else:
			print(rec_buff.decode())
			return 1
	else:
		print(command + ' no responce')

def send_tcp_message():
    try:
        power_on(power_key)

        # Setze den APN
        ser.write(('AT+CGDCONT=1,"IP","' + APN + '"\r\n').encode())
        time.sleep(1)
        if ser.inWaiting():
            rec_buff = ser.read(ser.inWaiting())
            print(rec_buff.decode())

        # Starte die PDP-Kontextaktivierung
        ser.write('AT+CGACT=1,1\r\n'.encode())
        time.sleep(1)
        if ser.inWaiting():
            rec_buff = ser.read(ser.inWaiting())
            print(rec_buff.decode())

        # Öffne eine TCP-Verbindung
        ser.write(('AT+CIPSTART="TCP","' + server_ip + '",' + Port + '\r\n').encode())
        time.sleep(2)
        if ser.inWaiting():
            rec_buff = ser.read(ser.inWaiting())
            print(rec_buff.decode())

    finally:
        ser.close()
        GPIO.cleanup()
        print('Good bye\n')

if __name__ == "__main__":
    send_tcp_message()
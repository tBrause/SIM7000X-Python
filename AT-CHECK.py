#!/usr/bin/env python3

import serial

ser = serial.Serial("/pi/serial0", baudrate=9600, timeout=1)
print("Serielle Schnittstelle aktiviert!")

ser.close()  # Nicht vergessen zu schließen, wenn du fertig bist!
print("Serielle Schnittstelle geschlossen.")
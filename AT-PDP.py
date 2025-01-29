#!/usr/bin/python

import serial
import time

# Konfiguriere die serielle Schnittstelle
SERIAL_PORT = "/dev/serial0"
BAUD_RATE = 9600
TIMEOUT = 1

# Initialisiere die serielle Verbindung
def initialize_serial():
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=TIMEOUT)
        print(f"Verbindung: {SERIAL_PORT}, {BAUD_RATE} Baud, Timeout: {TIMEOUT}s \n")
        return ser
    except Exception as e:
        print(f"Fehler beim Öffnen der seriellen Verbindung: {e}")
        return None

# Sende einen AT-Befehl und lese die Antwort
def send_at_command(ser, command, delay=1):
    try:
        #print(f"Sende Befehl: {command}")
        ser.write((command + "\r").encode())  # Sende den AT-Befehl mit Carriage Return
        time.sleep(delay)  # Warte auf die Antwort
        response = ser.read_all().decode().strip()  # Lies die Antwort
        if response:
            print(f"Antwort: {response}")
        else:
            print(f"Keine Antwort auf Befehl: {command}")
        return response
    except Exception as e:
        print(f"Fehler beim Senden des Befehls {command}: {e}")
        return ""

# Hauptfunktion für die Abfragen
def main():
    # Serielle Verbindung initialisieren
    ser = initialize_serial()
    if ser is None:
        return  # Beende das Programm, wenn die serielle Verbindung nicht geöffnet werden kann

    try:
      """
      //List of supported responses

AT+CGACT=?

 

//Wait for 1 second

WAIT=0

 

//Check the status of the profiles

AT+CGACT?

 

//Wait for 1 second

WAIT=1

 

//Activate PDP profile 3

AT+CGACT=1,3

 

//Wait for 4 seconds

WAIT=4

 

//Check status of PDP profiles

AT+CGACT?

 

//Wait for 1 second

WAIT=1

 

//Deactivate profile 3

AT+CGACT=0,3

 

//Wait for 3 seconds

WAIT=3

 

//Check status of PDP profiles

AT+CGACT?
"""
    finally:
        # Schließe die serielle Verbindung
        ser.close()
        print("# Serielle Verbindung geschlossen.\n")

# Skript starten
if __name__ == "__main__":
    main()

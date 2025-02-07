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
def send_at_command(ser, command, delay=3):
    try:
        #print(f"Sende Befehl: {command}")
        ser.write((command + "\r").encode())  # Sende den AT-Befehl mit Carriage Return
        time.sleep(delay)  # Warte auf die Antwort
        response = ser.read_all().decode().strip()  # Lies die Antwort und entferne Leerzeichen
        if not response:
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
        # Serielle Verbindung öffnen
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=5)
        print(f"Serielle Verbindung geöffnet: {SERIAL_PORT} mit Baudrate {BAUD_RATE}\n")

        
        # List of supported responses
        response = send_at_command(ser, "AT+CGACT=?", delay=3)
        print("List of supported responses:", response)
        
        # Check the status of the profiles (CGACT)
        response = send_at_command(ser, "AT+CGACT?", delay=3)
        print("Status of the profiles (CGACT):", response)
        
        # Activate PDP profile 3
        response = send_at_command(ser, "AT+CGACT=1,1", delay=3)
        print("Activate PDP profile 3:", response)
        
        # AT+CNACT=1,"cmnet"
        response = send_at_command(ser, 'AT+CNACT=1,"internet"', delay=3)
        print("Wireless connection:", response)
        
        # AT+CNACT? IP address
        response = send_at_command(ser, "AT+CNACT?", delay=3)
        print("Local IP address:", response)
        
        # Deactivate profile 3
        response = send_at_command(ser, "AT+CGACT=0,1", delay=3)
        print("Deactivate profile 3:", response)
        
        # Check status of PDP profiles
        response = send_at_command(ser, "AT+CGACT?", delay=3)
        print("Status of the profiles (CGACT):", response)

        
    except Exception as e:
        print(f"Fehler bei der Verarbeitung: {e}")
    finally:
        # Schließe die serielle Verbindung
        ser.close()
        print("# Serielle Verbindung geschlossen.\n")

# Skript starten
if __name__ == "__main__":
    main()

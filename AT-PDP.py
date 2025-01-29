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
        # Serielle Verbindung öffnen
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=5)
        print(f"Serielle Verbindung geöffnet: {SERIAL_PORT} mit Baudrate {BAUD_RATE}")

        
        # List of supported responses
        response = send_at_command(ser, "AT+CGACT=?")
        print("Antwort:", response)
        
    except Exception as e:
        print(f"Fehler bei der Verarbeitung: {e}")
    finally:
        # Schließe die serielle Verbindung
        ser.close()
        print("# Serielle Verbindung geschlossen.\n")

# Skript starten
if __name__ == "__main__":
    main()

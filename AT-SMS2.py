#!/usr/bin/env python3

import serial
import time

# Importiere die Konfiguration aus der Datei: ./conf/confDevice.json
import json

with open('./conf/confDevice.json') as json_file:
    data = json.load(json_file)
    SERIAL_PORT = data['SERIAL_PORT']
    BAUD_RATE = data['BAUD_RATE']
    PROVAPN = data['PROVAPN']
    PROVOPS = data['PROVOPS']
    SIMPIN = data['SIMPIN']

with open('./conf/confSIM.json') as json_file:
    data = json.load(json_file)
    BITRATE = data['BITRATE']

# Konfiguration der seriellen Schnittstelle
SERIAL_PORT = SERIAL_PORT
BAUD_RATE = BAUD_RATE
PHONE_NUMBER = "+491784576321"
MESSAGE = "Hallo! Dies ist eine Test-SMS vom SIM7000X."

def send_at_command(ser, command, expected_response="OK", timeout=3):
    """Sendet einen AT-Befehl und gibt die Antwort zurück."""
    ser.write((command + "\r\n").encode())
    time.sleep(0.5)
    response = ser.read(ser.in_waiting).decode(errors="ignore")
    
    print(f"> {command}")  # Debug-Ausgabe
    print(f"< {response}")  # Antwort anzeigen
    
    if expected_response in response:
        return response
    else:
        return f"Fehler oder keine Antwort erhalten: {response}"

try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=5)
    print(f"Serielle Verbindung geöffnet: {SERIAL_PORT} mit Baudrate {BAUD_RATE}")
    
    time.sleep(2)  # Wartezeit für Modulinitalisierung
    
    # Test: Ist das Modul bereit?
    for _ in range(5):
        response = send_at_command(ser, "AT")
        if "OK" in response:
            break
        time.sleep(2)
    
    # Falls keine Antwort: Modul ist nicht bereit
    if "OK" not in response:
        print("Fehler: Keine Antwort vom SIM7000X-Modul.")
        exit(1)

    # SMS-Modus auf Text setzen
    response = send_at_command(ser, "AT+CMGF=1")
    
    # Telefonnummer setzen und Nachricht senden
    print(f"Sende SMS an {PHONE_NUMBER}...")
    ser.write(f'AT+CMGS="{PHONE_NUMBER}"\r'.encode())
    time.sleep(2)  # Warten auf Eingabeaufforderung >
    
    ser.write((MESSAGE + "\x1A").encode())  # STRG+Z zum Senden
    time.sleep(5)  # Warte auf Modulantwort
    
    response = ser.read(ser.in_waiting).decode(errors="ignore")
    print("Antwort vom Modul:", response)

except Exception as e:
    print("Fehler:", e)

finally:
    if 'ser' in locals() and ser.is_open:
        ser.close()
        print("Serielle Verbindung geschlossen.")

#!/usr/bin/python

import RPi.GPIO as GPIO
import serial
import time

# Konfiguriere die serielle Schnittstelle
SERIAL_PORT = "/dev/ttyS0"  # Ersetze mit deinem Port (z. B. /dev/ttyS0 oder COM3)
BAUD_RATE = 9600
TIMEOUT = 1

# Initialisiere die serielle Verbindung
def initialize_serial():
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=TIMEOUT)
        print(f"✅ Serielle Verbindung geöffnet: {SERIAL_PORT}")
        return ser
    except Exception as e:
        print(f"❌ Fehler beim Öffnen der seriellen Verbindung: {e}")
        return None

# Sende einen AT-Befehl und lese die Antwort
def send_at_command(ser, command, delay=1):
    try:
        print(f"📤 Sende Befehl: {command}")
        ser.write((command + "\r").encode())  # Sende den AT-Befehl mit Carriage Return
        time.sleep(delay)  # Warte auf die Antwort
        response = ser.read_all().decode().strip()  # Lies die Antwort
        if response:
            print(f"📥 Antwort: {response}")
        else:
            print(f"⚠️ Keine Antwort auf Befehl: {command}")
        return response
    except Exception as e:
        print(f"❌ Fehler beim Senden des Befehls {command}: {e}")
        return ""

# Hauptfunktion für die Abfragen
def main():
    # Serielle Verbindung initialisieren
    ser = initialize_serial()
    if ser is None:
        return  # Beende das Programm, wenn die serielle Verbindung nicht geöffnet werden kann

    try:
        # Teste die grundlegende Kommunikation mit dem Modul
        print("🔄 Überprüfe grundlegende Verbindung mit AT-Befehl...")
        response = send_at_command(ser, "AT")
        if "OK" not in response:
            print("❌ Modem antwortet nicht auf 'AT'. Bitte Verbindung prüfen.")
            return

        # 1. Status der SIM-Karte
        print("\n1️⃣ Status der SIM-Karte:")
        send_at_command(ser, "AT+CPIN?")

        # 2. Ist die SIM-Karte eingelegt?
        print("\n2️⃣ Ist die SIM-Karte eingelegt?")
        send_at_command(ser, "AT+CSMINS?")

        # 3. Aktuellen Netzbetreiber anzeigen
        print("\n3️⃣ Aktuellen Netzbetreiber anzeigen:")
        send_at_command(ser, "AT+COPS?")

        # 4. Signalqualität abfragen
        print("\n4️⃣ Signalqualität abfragen:")
        send_at_command(ser, "AT+CSQ")

    finally:
        # Schließe die serielle Verbindung
        ser.close()
        print("\n✅ Serielle Verbindung geschlossen.")

# Skript starten
if __name__ == "__main__":
    main()

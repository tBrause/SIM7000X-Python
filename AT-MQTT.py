#!/usr/bin/python

# import RPi.GPIO as GPIO
import serial
import time

# Konfiguriere die serielle Schnittstelle
SERIAL_PORT = "/dev/serial0"
BAUD_RATE = 9600
TIMEOUT = 1

# Konfiguriere die Zugangsdaten für den MQTT-Broker
MQTT_SERVER = "test.mosquitto.org"
MQTT_PORT = 1883
MQTT_TOPIC = "test"
MQTT_MESSAGE = "Hello, MQTT!"

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
        # Teste die grundlegende Kommunikation mit dem Modul
        print("Teste die grundlegende Kommunikation mit dem Modul")
        response = send_at_command(ser, "AT")
        if "OK" not in response:
            print("Modem antwortet nicht auf 'AT'. Bitte Verbindung prüfen.")
            return

        # 1. Status der SIM-Karte
        print("\n# Status der SIM-Karte:")
        send_at_command(ser, "AT+CPIN?")

        # 2. Aktiviere MQTT
        print("\n# Aktiviere MQTT")
        send_at_command(ser, f"AT+CGDCONT=1,'IP','internet'")
        send_at_command(ser, f"AT+CGATT=1")
        send_at_command(ser, f"AT+CMQTTACCQ=0,'client_id'")
        #send_at_command(ser, f"AT+SMCONF=?")
        # AT+SMCONF? READ
        send_at_command(ser, f"AT+CNACT?")
        # AT+SMCONF=<n>[,<m>] WRITE
        #send_at_command(ser, f"AT+CMQTTSTART")
        #send_at_command(ser, f"AT+SMCONN")
        #send_at_command(ser, f"AT+CMQTTACCQ=0,0,\"{MQTT_SERVER}\"")
        #send_at_command(ser, f"AT+CMQTTCONNECT=0,\"tcp://{MQTT_SERVER}:{MQTT_PORT}\",60,1")
        #send_at_command(ser, f"AT+CMQTTSUB=0,1,\"{MQTT_TOPIC}\",1")
        #send_at_command(ser, f"AT+CMQTTTOPIC=0,0,\"{MQTT_TOPIC}\"")
        #send_at_command(ser, f"AT+CMQTTPAYLOAD=0,0,\"{MQTT_MESSAGE}\"")
        #send_at_command(ser, f"AT+CMQTTPUB=0,1,60")
        
    finally:
        # Schließe die serielle Verbindung
        ser.close()
        print("# Serielle Verbindung geschlossen.\n")

# Skript starten
if __name__ == "__main__":
    main()

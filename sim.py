import serial
import time

# Konfiguriere die serielle Schnittstelle
SERIAL_PORT = "/dev/ttyS0"  # Ersetze mit dem entsprechenden Port (z. B. COM3 für Windows)
BAUD_RATE = 9600
TIMEOUT = 1

# Initialisiere die serielle Verbindung
def initialize_serial():
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=TIMEOUT)
        print(f"Serielle Verbindung geöffnet: {SERIAL_PORT}")
        return ser
    except Exception as e:
        print(f"Fehler beim Öffnen der seriellen Verbindung: {e}")
        return None

# Sende einen AT-Befehl und lese die Antwort
def send_at_command(ser, command, delay=0.5):
    try:
        ser.write((command + "\r").encode())
        time.sleep(delay)
        response = ser.read_all().decode().strip()
        return response
    except Exception as e:
        return f"Fehler beim Senden des Befehls {command}: {e}"

# Hauptfunktion für die Abfragen
def main():
    # Serielle Verbindung initialisieren
    ser = initialize_serial()
    if ser is None:
        return

    try:
        # 1. Status der SIM-Karte
        print("1. Status der SIM-Karte:")
        response = send_at_command(ser, "AT+CPIN?")
        print(response)

        # 2. Ist die Karte eingelegt?
        print("\n2. Ist die Karte eingelegt?")
        response = send_at_command(ser, "AT+CSMINS?")
        print(response)

        # 3. Aktuellen Netzbetreiber anzeigen
        print("\n3. Aktuellen Netzbetreiber anzeigen:")
        response = send_at_command(ser, "AT+COPS?")
        print(response)

        # 4. Signalqualität abfragen
        print("\n4. Signalqualität abfragen:")
        response = send_at_command(ser, "AT+CSQ")
        print(response)

    finally:
        # Serielle Verbindung schließen
        ser.close()
        print("\nSerielle Verbindung geschlossen.")

# Skript starten
if __name__ == "__main__":
    main()

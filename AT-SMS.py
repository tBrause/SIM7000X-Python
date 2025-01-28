import serial
import time

# Konfiguration der seriellen Schnittstelle
SERIAL_PORT = "/dev/serial0"  # Anpassen, falls anders
BAUD_RATE = 9600

# Telefonnummer für den SMS-Versand
PHONE_NUMBER = "+491784576321"  # Ersetze mit der echten Nummer

# Nachricht
MESSAGE = "Hallo! Dies ist eine Test-SMS vom SIM7000X."

def send_at_command(ser, command, expected_response="OK", timeout=3):
    """Sendet einen AT-Befehl und gibt die Antwort zurück."""
    ser.write((command + "\r\n").encode())
    time.sleep(0.5)
    response = ser.read(ser.in_waiting).decode(errors="ignore")
    
    if expected_response in response:
        return response
    else:
        return f"Fehler oder keine Antwort erhalten: {response}"

try:
    # Serielle Verbindung öffnen
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=5)
    print(f"Serielle Verbindung geöffnet: {SERIAL_PORT} mit Baudrate {BAUD_RATE}")

    # Prüfen, ob das Modul bereit ist
    response = send_at_command(ser, "AT")
    print("Antwort:", response)

    # SMS-Modus auf Text setzen
    response = send_at_command(ser, "AT+CMGF=1")
    print("Setze SMS-Modus:", response)

    # Telefonnummer setzen und Nachricht senden
    print(f"Sende SMS an {PHONE_NUMBER}...")
    ser.write(f'AT+CMGS="{PHONE_NUMBER}"\r'.encode())
    time.sleep(1)
    ser.write((MESSAGE + "\x1A").encode())  # \x1A ist STRG+Z zum Senden
    time.sleep(3)

    # Antwort des Moduls auslesen
    response = ser.read(ser.in_waiting).decode(errors="ignore")
    print("Antwort vom Modul:", response)

except Exception as e:
    print("Fehler:", e)

finally:
    # Serielle Verbindung schließen
    if 'ser' in locals() and ser.is_open:
        ser.close()
        print("Serielle Verbindung geschlossen.")

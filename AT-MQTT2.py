import serial
import time

# Konfiguration für die serielle Schnittstelle
SERIAL_PORT = "/dev/serial0"  # Anpassen, falls nötig
BAUD_RATE = 9600
TIMEOUT = 1

# MQTT-Broker Konfiguration
BROKER = "mqtt.c2.energywan.de"
PORT = "1883"
CLIENT_ID = "SIM7000_MQTT_Client"
TOPIC = "python/mqtt"
MESSAGE = "Hello from SIM7000X!"

def send_at_command(ser, command, expected_response, timeout=2):
    """
    Sendet einen AT-Befehl und wartet auf die erwartete Antwort.
    """
    ser.write((command + "\r\n").encode())  # Senden des Befehls
    time.sleep(0.1)
    start_time = time.time()
    response = ""
    while time.time() - start_time < timeout:
        if ser.in_waiting > 0:
            response += ser.read(ser.in_waiting).decode(errors="ignore")
            if expected_response in response:
                return response
    return response  # Rückgabe der erhaltenen Antwort (auch wenn sie nicht passt)

def setup_mqtt(ser):
    """
    Einrichtung der MQTT-Verbindung mit dem SIM7000-Modul.
    """
    # 1. MQTT konfigurieren
    print("1. MQTT konfigurieren...")
    response = send_at_command(ser, f'AT+CMQTTSTART', "OK", timeout=5)
    print("Antwort:", response)
    if "ERROR" in response:
        print("Fehler beim Starten des MQTT-Services.")
        return False

    # 2. MQTT-Client erstellen
    print("2. MQTT-Client erstellen...")
    response = send_at_command(ser, f'AT+CMQTTACCQ=0,"{CLIENT_ID}"', "OK", timeout=5)
    print("Antwort:", response)
    if "ERROR" in response:
        print("Fehler beim Erstellen des MQTT-Clients.")
        return False

    # 3. Mit dem MQTT-Broker verbinden
    print("3. Mit dem MQTT-Broker verbinden...")
    response = send_at_command(ser, f'AT+CMQTTCONNECT=0,"tcp://{BROKER}:{PORT}",60,1', "+CMQTTCONNECT: 0,0", timeout=10)
    print("Antwort:", response)
    if "+CMQTTCONNECT: 0,0" not in response:
        print("Fehler beim Verbinden mit dem MQTT-Broker.")
        return False

    return True

def publish_message(ser):
    """
    Nachricht an den MQTT-Broker senden.
    """
    # 1. Länge der Nachricht bestimmen
    print("1. Nachricht vorbereiten...")
    message_length = len(MESSAGE)
    response = send_at_command(ser, f'AT+CMQTTTOPIC=0,{len(TOPIC)}', ">", timeout=5)
    print("Antwort:", response)
    if ">" not in response:
        print("Fehler beim Setzen des Topics.")
        return False

    # 2. Topic senden
    ser.write((TOPIC + "\r\n").encode())
    time.sleep(1)

    # 3. Nachricht an das Topic senden
    print("2. Nachricht senden...")
    response = send_at_command(ser, f'AT+CMQTTPAYLOAD=0,{message_length}', ">", timeout=5)
    print("Antwort:", response)
    if ">" not in response:
        print("Fehler beim Vorbereiten des Nachrichteninhalts.")
        return False

    # 4. Nachricht übertragen
    ser.write((MESSAGE + "\r\n").encode())
    time.sleep(1)

    # 5. Nachricht veröffentlichen
    print("3. Nachricht veröffentlichen...")
    response = send_at_command(ser, 'AT+CMQTTPUB=0,1,60', "+CMQTTPUB: 0,0", timeout=5)
    print("Antwort:", response)
    if "+CMQTTPUB: 0,0" not in response:
        print("Fehler beim Veröffentlichen der Nachricht.")
        return False

    print("Nachricht erfolgreich gesendet!")
    return True

def close_mqtt(ser):
    """
    MQTT-Verbindung schließen.
    """
    print("MQTT-Verbindung schließen...")
    send_at_command(ser, "AT+CMQTTDISC=0,60", "+CMQTTDISC: 0,0", timeout=5)
    send_at_command(ser, "AT+CMQTTREL=0", "OK", timeout=5)
    send_at_command(ser, "AT+CMQTTSTOP", "OK", timeout=5)
    print("MQTT-Service gestoppt.")

def main():
    try:
        # Serielle Verbindung öffnen
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=TIMEOUT)
        print(f"Serielle Verbindung geöffnet: {SERIAL_PORT} mit Baudrate {BAUD_RATE}")

        # MQTT einrichten
        if setup_mqtt(ser):
            # Nachricht veröffentlichen
            publish_message(ser)

        # MQTT beenden
        close_mqtt(ser)

        # Serielle Verbindung schließen
        ser.close()
        print("Serielle Verbindung geschlossen.")

    except Exception as e:
        print(f"Fehler: {e}")

if __name__ == "__main__":
    main()

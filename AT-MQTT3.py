import serial
import time

def send_at_command(ser, command, expected_response, timeout=5):
    ser.write((command + "\r\n").encode())
    time.sleep(0.5)
    end_time = time.time() + timeout
    response = ""
    while time.time() < end_time:
        if ser.in_waiting > 0:
            response += ser.read(ser.in_waiting).decode()
            if expected_response in response:
                return response
    return response

# Serielle Verbindung einrichten
serial_port = "/dev/serial0"
baud_rate = 9600

ser = serial.Serial(serial_port, baud_rate, timeout=1)
print(f"Serielle Verbindung geöffnet: {serial_port} mit Baudrate {baud_rate}")

try:
    # Debugging aktivieren
    """
    response = send_at_command(ser, "AT+SMLOG=1", "OK", timeout=5)
    print("Debugging aktiviert:", response)
    """

    # Netzwerkregistrierung überprüfen
    print("Netzwerk-Status überprüfen...")
    response = send_at_command(ser, "AT+CREG?", "+CREG: 0,1", timeout=5)
    print("Netzwerk-Status:", response)
    if "+CREG: 0,1" not in response:
        print("Fehler: Modul nicht im Netzwerk registriert.")
        exit()

    # APN konfigurieren
    print("APN konfigurieren...")
    response = send_at_command(ser, 'AT+CGDCONT=1,"IP","internet"', "OK", timeout=5)
    print("Antwort:", response)
    
    # Datenverbindung aktivieren
    print("Datenverbindung aktivieren...")
    response = send_at_command(ser, "AT+CGACT=1,1", "OK", timeout=5)
    print("Datenverbindung aktiviert:", response)
    if "OK" not in response:
        print("Fehler: Datenverbindung konnte nicht aktiviert werden.")
        exit()

    # MQTT-Parameter konfigurieren
    print("MQTT-Parameter konfigurieren...")
    response = send_at_command(ser, 'AT+SMCONF="URL","test.mosquitto.org","1883"', "OK", timeout=5)
    print("Antwort:", response)
    
    response = send_at_command(ser, 'AT+SMCONF="CLIENTID","SIM7000X_Client_123"', "OK", timeout=5)
    print("Antwort:", response)

    response = send_at_command(ser, 'AT+SMCONF="KEEPTIME",60', "OK", timeout=5)
    print("Antwort:", response)

    response = send_at_command(ser, 'AT+SMCONF="CLEANSS",1', "OK", timeout=5)
    print("Antwort:", response)

    # Optional: Authentifizierung
    # response = send_at_command(ser, 'AT+SMCONF="USERNAME","dein_benutzername"', "OK", timeout=5)
    # print("Antwort:", response)
    # response = send_at_command(ser, 'AT+SMCONF="PASSWORD","dein_passwort"', "OK", timeout=5)
    # print("Antwort:", response)

    # MQTT-Dienst überprüfen
    print("MQTT-Dienst überprüfen...")
    response = send_at_command(ser, 'AT+SMSTATE?', "OK", timeout=5)
    print("Antwort:", response)
    
    if "OK" not in response:
        print("Fehler: MQTT-Dienst konnte nicht aktiviert werden.")
        exit()
    
    
    # MQTT-Status aktivieren
    print("MQTT-Status aktivieren...")
    response = send_at_command(ser, "AT+SMSTATE?", "+SMSTATE: 1", timeout=5)
    print("Antwort:", response)
    if "+SMSTATE: 1" not in response:
        print("Fehler: MQTT-Dienst ist nicht aktiviert.")
        exit()

    # MQTT-Verbindung herstellen
    print("MQTT-Verbindung herstellen...")
    response = send_at_command(ser, "AT+SMCONN", "OK", timeout=20)  # Erhöhter Timeout
    print("Antwort:", response)
    if "ERROR" in response:
        print("Fehler bei der MQTT-Verbindung.")
        exit()

    # Nachricht veröffentlichen
    print("Nachricht veröffentlichen...")
    response = send_at_command(ser, 'AT+SMPUB="python/mqtt",5,1,0', ">", timeout=5)
    print("Antwort:", response)
    if ">" in response:
        ser.write("Hello".encode())  # Sende die Nachricht
        time.sleep(0.5)

    # MQTT-Verbindung trennen
    print("MQTT-Verbindung trennen...")
    response = send_at_command(ser, "AT+SMDISC", "OK", timeout=5)
    print("Antwort:", response)

finally:
    # Serielle Verbindung schließen
    ser.close()
    print("Serielle Verbindung geschlossen.")
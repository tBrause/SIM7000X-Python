import serial
import time

# Funktion zum Senden von AT-Befehlen
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
    
    response = send_at_command(ser, "AT+CREG?", "OK", timeout=5)
    print("Netzwerk-Status:", response)


    # Status des MQTT-Dienstes abfragen
    print("Status des MQTT-Dienstes abfragen...")
    response = send_at_command(ser, "AT+SMSTATE?", "STATE: 0", timeout=5)
    print("Antwort:", response)
    
    # 1. APN konfigurieren
    print("APN konfigurieren...")
    response = send_at_command(ser, 'AT+CGDCONT=1,"IP","internet"', "OK", timeout=5)
    print("Antwort:", response)
    
    response = send_at_command(ser, "AT+CGACT=1,1", "OK", timeout=5)
    print("Datenverbindung aktiviert:", response)
    
    response = send_at_command(ser, "AT+CIFSR", ".", timeout=5)
    print("IP-Adresse:", response)


    # 2. MQTT-Parameter konfigurieren
    print("MQTT-Parameter konfigurieren...")
    response = send_at_command(ser, 'AT+SMCONF="URL","tcp://emqx.c2.energywan.de","1883"', "OK", timeout=5)
    print("Antwort:", response)
    
    response = send_at_command(ser, 'AT+SMCONF="CLIENTID","SIM7000X_Client"', "OK", timeout=5)
    print("Antwort:", response)

    # Optional: Benutzername und Passwort, falls benötigt
    """
    response = send_at_command(ser, 'AT+SMCONF="USERNAME","your_username"', "OK", timeout=5)
    print("Antwort:", response)
    response = send_at_command(ser, 'AT+SMCONF="PASSWORD","your_password"', "OK", timeout=5)
    print("Antwort:", response)
    
    response = send_at_command(ser, 'AT+SMCONF="USERNAME","your_username"', "OK", timeout=5)
    print("Antwort:", response)
    response = send_at_command(ser, 'AT+SMCONF="PASSWORD","your_password"', "OK", timeout=5)
    print("Antwort:", response)
    """
    # 3. MQTT-Verbindung herstellen
    print("MQTT-Verbindung herstellen...")
    response = send_at_command(ser, "AT+SMCONN", "OK", timeout=10)
    print("Antwort:", response)
    if "ERROR" in response:
        print("Fehler bei der MQTT-Verbindung.")
        exit()

    # 4. Nachricht veröffentlichen
    print("Nachricht veröffentlichen...")
    response = send_at_command(ser, 'AT+SMPUB="python/mqtt",5,1,0', ">", timeout=5)  # 5 = Nachrichtengröße
    print("Antwort:", response)
    if ">" in response:
        ser.write("Hello".encode())  # Sende die Nachricht
        time.sleep(0.5)

    # 5. MQTT-Verbindung trennen
    print("MQTT-Verbindung trennen...")
    response = send_at_command(ser, "AT+SMDISC", "OK", timeout=5)
    print("Antwort:", response)

finally:
    # Serielle Verbindung schließen
    ser.close()
    print("Serielle Verbindung geschlossen.")

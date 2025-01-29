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
    
    # Open wireless connection
    print("Open wireless connection...")
    response = send_at_command(ser, "AT+CNACT=1", "OK", timeout=5)
    print("Wireless connection:", response)
    

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

    # TCP Verbindung aufbauen
    print("TCP Verbindung aufbauen...")
    response = send_at_command(ser, 'AT+CIPSTART="TCP","sanberlin.com","80"', "CONNECT OK", timeout=10)
    print("TCP Verbindung aufgebaut:", response)
    if "CONNECT OK" not in response:
        print("Fehler: TCP Verbindung konnte nicht aufgebaut werden.")
        exit()

    # MQTT-Parameter konfigurieren
    print("MQTT-Parameter konfigurieren...")
    send_at_command(ser, 'AT+SMCONF="URL","emqx.c2.energywan.de","1883"', "OK", timeout=5)
    send_at_command(ser, 'AT+SMCONF="CLIENTID","SIM7000X_Client_123"', "OK", timeout=5)
    send_at_command(ser, 'AT+SMCONF="KEEPTIME",60', "OK", timeout=5)
    send_at_command(ser, 'AT+SMCONF="CLEANSS",0', "OK", timeout=5)
    send_at_command(ser, 'AT+SMCONF="QOS",0', "OK", timeout=5)
    send_at_command(ser, 'AT+SMCONF="TOPIC","python/mqtt"', "OK", timeout=5)
    send_at_command(ser, 'AT+SMCONF="MESSAGE","Hello"', "OK", timeout=5)
    send_at_command(ser, 'AT+SMCONF="RETAIN",0', "OK", timeout=5)
    send_at_command(ser, 'AT+SMCONF="USERNAME","your_username"', "OK", timeout=5)
    send_at_command(ser, 'AT+SMCONF="PASSWORD","your_password"', "OK", timeout=5)

    # MQTT-Status überprüfen
    print("MQTT-Dienst überprüfen...")
    response = send_at_command(ser, 'AT+SMSTATE?', "OK", timeout=5)
    print("Antwort:", response)
    
    if "+SMSTATE: 1" not in response:
        print("Fehler: MQTT-Dienst ist nicht aktiv.")
        
    # Falls MQTT-Dienst nicht aktiv ist, manuell starten
    if "+SMSTATE: 0" in response:
      print("MQTT-Dienst ist nicht aktiv. Starte den Dienst...")
    
      response = send_at_command(ser, "AT+SMDISC", "OK", timeout=5)  # Falls vorher verbunden
      print("MQTT-Reset:", response)

      response = send_at_command(ser, "AT+SMCONN", "OK", timeout=10)  # Versuche Verbindung erneut
      print("MQTT-Verbindung:", response)
    
      response = send_at_command(ser, "AT+SMSTATE?", "OK", timeout=5)  # Status erneut prüfen
      print("Neuer MQTT-Status:", response)

    if "+SMSTATE: 1" not in response:
        print("Fehler: MQTT-Dienst konnte nicht aktiviert werden.")
        exit()

    
    # MQTT-Verbindung herstellen
    print("MQTT-Verbindung herstellen...")
    response = send_at_command(ser, "AT+SMCONN", "OK", timeout=20)  # Erhöhter Timeout
    print("Antwort:", response)
    time.sleep(3)  # Warte, um sicherzustellen, dass die Verbindung aufgebaut ist
    if "ERROR" in response:
        print("Fehler bei der MQTT-Verbindung.")
        exit()

    # MQTT-Status erneut überprüfen
    response = send_at_command(ser, "AT+SMSTATE?", "+SMSTATE: 1", timeout=5)
    if "+SMSTATE: 1" not in response:
        print("Fehler: MQTT ist nicht aktiv.")
        exit()
    
    # Nachricht veröffentlichen
    print("Nachricht veröffentlichen...")
    response = send_at_command(ser, 'AT+SMPUB="python/mqtt",5,1,0', ">", timeout=5)
    print("Antwort:", response)
    if ">" in response:
        ser.write("Hello\r\n".encode())  # Nachricht senden mit "\r\n"
        time.sleep(0.5)

    # MQTT-Verbindung trennen, aber nur wenn aktiv
    if "+SMSTATE: 1" in send_at_command(ser, "AT+SMSTATE?", "+SMSTATE: 1", timeout=5):
        print("MQTT-Verbindung trennen...")
        response = send_at_command(ser, "AT+SMDISC", "OK", timeout=5)
        print("Antwort:", response)

finally:
    # Serielle Verbindung schließen
    ser.close()
    print("Serielle Verbindung geschlossen.")

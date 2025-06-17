import serial
import time

# ---- KONFIGURATION ----
SERIAL_PORT = "/dev/serial0"
BAUDRATE = 115200
APN = "lpwa.vodafone.com"

MQTT_server = "emqx.c2.energywan.de"
MQTT_port = 1883
MQTT_user = "sww_ZL6xVtWQjN"
MQTT_password = "sukFYfDzvrnsy8hD"
MQTT_client = "TOMTEST01"
MQTT_topic = "hello"
MQTT_msg = "Hallo von SIM7000E!"

def send_at(ser, cmd, timeout=2, show_cmd=True):
    if show_cmd:
        print(f"--> {cmd.strip()}")
    ser.write((cmd + '\r\n').encode())
    time.sleep(timeout)
    out = b""
    while ser.in_waiting:
        out += ser.read(ser.in_waiting)
        time.sleep(0.1)
    try:
        decoded = out.decode(errors='ignore')
        print(f"<-- {decoded.strip()}")
        return decoded
    except Exception as e:
        print(f"Decode-Fehler: {e}")
        return ""
    
def wait_for_ok(response, stepname):
    if "OK" in response:
        print(f"[OK] {stepname}")
        return True
    elif "ERROR" in response:
        print(f"[FEHLER] {stepname}: ERROR")
        return False
    else:
        print(f"[WARNUNG] {stepname}: Unerwartete Antwort")
        return False

def main():
    print(f"Serielle Verbindung öffnen: {SERIAL_PORT} @ {BAUDRATE}")
    ser = serial.Serial(SERIAL_PORT, BAUDRATE, timeout=1)

    # Modul testen
    resp = send_at(ser, "AT")
    if not wait_for_ok(resp, "Modultest"):
        ser.close()
        return

    # APN setzen
    resp = send_at(ser, f'AT+CGDCONT=1,"IP","{APN}"')
    if not wait_for_ok(resp, "APN setzen"):
        ser.close()
        return

    # Status-Check
    print("\n== NETZWERKSTATUS CHECK ==\n")
    send_at(ser, "AT+CPIN?")
    send_at(ser, "AT+CSQ")
    send_at(ser, "AT+COPS?")
    send_at(ser, "AT+CGATT?")
    send_at(ser, "AT+CGACT?")
    send_at(ser, "AT+CGDCONT?")
    print("\n===========================\n")

    # MQTT-Stack starten
    print("Starte MQTT-Stack...")
    resp = send_at(ser, "AT+CMQTTSTART", timeout=4)
    if "ERROR" in resp:
        print("MQTT-Stack konnte nicht gestartet werden.")
        ser.close()
        return
    if "CMQTTSTART: 0" not in resp:
        print("Achtung: Unerwartete Antwort beim Start des MQTT-Stacks.")
        # Warte nochmal kurz und lese evtl. ausstehende Daten aus
        time.sleep(3)
        while ser.in_waiting:
            print("<-- " + ser.read(ser.in_waiting).decode(errors='ignore').strip())

    # MQTT-Status prüfen
    resp = send_at(ser, "AT+CMQTTSTATUS?")
    if "ERROR" in resp:
        print("MQTT-Status konnte nicht abgefragt werden. Beende.")
        # MQTT-Stack stoppen
        send_at(ser, "AT+CMQTTSTOP")
        ser.close()
        return

    # MQTT Client anmelden
    resp = send_at(ser, f'AT+CMQTTACCQ=0,"{MQTT_client}"')
    if not wait_for_ok(resp, "MQTT-Client anmelden"):
        send_at(ser, "AT+CMQTTSTOP")
        ser.close()
        return

    # Mit Broker verbinden
    print("Verbinde mit MQTT-Broker...")
    connect_cmd = f'AT+CMQTTCONNECT=0,"tcp://{MQTT_server}:{MQTT_port}",60,1,"{MQTT_user}","{MQTT_password}"'
    resp = send_at(ser, connect_cmd, timeout=5)
    if "OK" not in resp:
        print("Fehler bei der Verbindung zum MQTT-Broker.")
        send_at(ser, "AT+CMQTTDISCONN=0")
        send_at(ser, "AT+CMQTTSTOP")
        ser.close()
        return

    # Publish vorbereiten
    topic_len = len(MQTT_topic)
    resp = send_at(ser, f'AT+CMQTTTOPIC=0,{topic_len}')
    if ">" in resp:
        ser.write(MQTT_topic.encode())
        time.sleep(1)
        print(f"<-- Topic gesendet: {MQTT_topic}")
    else:
        print("Fehler bei MQTT-TOPIC.")
        send_at(ser, "AT+CMQTTDISCONN=0")
        send_at(ser, "AT+CMQTTSTOP")
        ser.close()
        return

    msg_len = len(MQTT_msg)
    resp = send_at(ser, f'AT+CMQTTMSG=0,{msg_len}')
    if ">" in resp:
        ser.write(MQTT_msg.encode())
        time.sleep(1)
        print(f"<-- Nachricht gesendet: {MQTT_msg}")
    else:
        print("Fehler bei MQTT-MSG.")
        send_at(ser, "AT+CMQTTDISCONN=0")
        send_at(ser, "AT+CMQTTSTOP")
        ser.close()
        return

    # Publish
    resp = send_at(ser, "AT+CMQTTPUB=0,1,60", timeout=3)
    if "OK" in resp:
        print("[OK] Nachricht veröffentlicht!")
    else:
        print("Fehler beim Publish!")

    # MQTT trennen und stoppen
    send_at(ser, "AT+CMQTTDISCONN=0")
    send_at(ser, "AT+CMQTTSTOP")
    ser.close()
    print("Fertig, Verbindung geschlossen.")

if __name__ == "__main__":
    main()

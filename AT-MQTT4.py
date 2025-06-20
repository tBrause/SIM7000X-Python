import serial
import time

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

def wait_for_ip(ser, tries=5, sleep=2):
    for i in range(tries):
        ipresp = send_at(ser, "AT+CGPADDR")
        if "+CGPADDR: 1," in ipresp and "0.0.0.0" not in ipresp:
            print(f"[OK] Echte IP nach {i+1} Versuchen: {ipresp.strip()}")
            return True
        time.sleep(sleep)
    print("[FEHLER] Nach mehrfachem Versuch keine gültige IP – MQTT kann nicht gestartet werden.")
    return False

def main():
    print(f"Serielle Verbindung öffnen: {SERIAL_PORT} @ {BAUDRATE}")
    ser = serial.Serial(SERIAL_PORT, BAUDRATE, timeout=1)

    # 1. Modul neu starten und warten, bis es antwortet
    send_at(ser, "AT+CFUN=1,1", timeout=8)
    print("Modul wird neu gestartet – bitte 35 Sekunden warten...")
    time.sleep(35)

    def wait_for_modem_ready(ser, max_tries=20):
        for i in range(max_tries):
            resp = send_at(ser, "AT", timeout=1, show_cmd=False)
            if "OK" in resp:
                print(f"[OK] Modem antwortet nach {i+1} Versuchen.")
                return True
            else:
                time.sleep(2)
        print("[FEHLER] Modem antwortet nicht nach Reset.")
        return False

    if not wait_for_modem_ready(ser):
        ser.close()
        return

    send_at(ser, 'AT+CNMP=38')  # LTE Only
    send_at(ser, 'AT+CMNB=3')   # Cat-M1 only
    time.sleep(2)

    send_at(ser, "ATI")
    send_at(ser, "AT+CMQTTVER")

    
    # 2. APN für PDP-Kontext 1 setzen
    resp = send_at(ser, f'AT+CGDCONT=1,"IP","{APN}"')
    if not wait_for_ok(resp, "APN setzen"):
        ser.close()
        return

    # 2b. Operator auf Vodafone NB-IoT zwingen (OPS 26202)
    resp = send_at(ser, 'AT+COPS=1,2,"26202"', timeout=20)
    if not wait_for_ok(resp, "Operator setzen"):
        print("[WARNUNG] Operator konnte nicht explizit gesetzt werden (evtl. bereits eingebucht)")

    # 3. Kontext 1 deaktivieren und Status checken
    send_at(ser, "AT+CGACT=0,1")
    time.sleep(7)
    send_at(ser, "AT+CGACT?")
    send_at(ser, "AT+CGDCONT?")
    send_at(ser, "AT+CGPADDR")

    # 4. Kontext 1 aktivieren
    resp = send_at(ser, "AT+CGACT=1,1", timeout=5)
    if not wait_for_ok(resp, "PDP-Kontext aktivieren"):
        ser.close()
        return

    # 5. Auf echte IP warten
    if not wait_for_ip(ser):
        ser.close()
        return

    # --- MQTT-Ablauf ---
    print("Starte MQTT-Stack...")
    resp = send_at(ser, "AT+CMQTTSTART", timeout=5)
    if "ERROR" in resp:
        print("[FEHLER] MQTT-Stack konnte nicht gestartet werden.")
        ser.close()
        return
    if "CMQTTSTART: 0" not in resp:
        print("[WARNUNG] Unerwartete Antwort beim Start des MQTT-Stacks.")

    # MQTT-Client anmelden
    resp = send_at(ser, f'AT+CMQTTACCQ=0,"{MQTT_client}"')
    if not wait_for_ok(resp, "MQTT-Client anmelden"):
        send_at(ser, "AT+CMQTTSTOP")
        ser.close()
        return

    # Mit MQTT-Broker verbinden
    print("Verbinde mit MQTT-Broker...")
    connect_cmd = f'AT+CMQTTCONNECT=0,"tcp://{MQTT_server}:{MQTT_port}",60,1,"{MQTT_user}","{MQTT_password}"'
    resp = send_at(ser, connect_cmd, timeout=5)
    if "OK" not in resp:
        print("[FEHLER] Verbindung zum MQTT-Broker fehlgeschlagen.")
        send_at(ser, "AT+CMQTTDISCONN=0")
        send_at(ser, "AT+CMQTTSTOP")
        ser.close()
        return

    # Topic senden
    topic_len = len(MQTT_topic)
    resp = send_at(ser, f'AT+CMQTTTOPIC=0,{topic_len}')
    if ">" in resp:
        ser.write(MQTT_topic.encode())
        time.sleep(1)
        print(f"<-- Topic gesendet: {MQTT_topic}")
    else:
        print("[FEHLER] Fehler bei MQTT-TOPIC.")
        send_at(ser, "AT+CMQTTDISCONN=0")
        send_at(ser, "AT+CMQTTSTOP")
        ser.close()
        return

    # Nachricht senden
    msg_len = len(MQTT_msg)
    resp = send_at(ser, f'AT+CMQTTMSG=0,{msg_len}')
    if ">" in resp:
        ser.write(MQTT_msg.encode())
        time.sleep(1)
        print(f"<-- Nachricht gesendet: {MQTT_msg}")
    else:
        print("[FEHLER] Fehler bei MQTT-MSG.")
        send_at(ser, "AT+CMQTTDISCONN=0")
        send_at(ser, "AT+CMQTTSTOP")
        ser.close()
        return

    # Publish
    resp = send_at(ser, "AT+CMQTTPUB=0,1,60", timeout=3)
    if "OK" in resp:
        print("[OK] Nachricht veröffentlicht!")
    else:
        print("[FEHLER] Fehler beim Publish!")

    # Aufräumen
    send_at(ser, "AT+CMQTTDISCONN=0")
    send_at(ser, "AT+CMQTTSTOP")
    ser.close()
    print("Fertig, Verbindung geschlossen.")

if __name__ == "__main__":
    main()

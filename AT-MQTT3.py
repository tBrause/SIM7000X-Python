import serial
import time

SERIAL_PORT = "/dev/serial0"
BAUDRATE = 115200
APN = "lpwa.vodafone.com"   # Oder "internet"
CONTEXT = 1                 # Oder 0 für Test

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

    # 0. Reboot-Modul
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

    # 1. Modul testen
    resp = send_at(ser, "AT")
    if not wait_for_ok(resp, "Modultest"):
        ser.close()
        return

    # 2. APN für PDP-Kontext setzen
    resp = send_at(ser, f'AT+CGDCONT={CONTEXT},"IP","{APN}"')
    if not wait_for_ok(resp, "APN setzen"):
        ser.close()
        return

    # 3. Kontext deaktivieren
    send_at(ser, f"AT+CGACT=0,{CONTEXT}")
    time.sleep(8)

    # Status abfragen
    send_at(ser, f"AT+CGACT?")
    send_at(ser, f"AT+CGDCONT?")
    send_at(ser, f"AT+CGPADDR")

    # 4. Kontext aktivieren
    resp = send_at(ser, f"AT+CGACT=1,{CONTEXT}", timeout=6)
    if not wait_for_ok(resp, "PDP-Kontext aktivieren"):
        ser.close()
        return

    # Rest des Scripts wie gehabt...

if __name__ == "__main__":
    main()

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

def main():
    print(f"Serielle Verbindung öffnen: {SERIAL_PORT} @ {BAUDRATE}")
    ser = serial.Serial(SERIAL_PORT, BAUDRATE, timeout=1)
    send_at(ser, "AT")
    send_at(ser, f'AT+CGDCONT=1,"IP","{APN}"')
    # Das war's. Jetzt sofort MQTT-Stack!
    resp = send_at(ser, "AT+CMQTTSTART", timeout=5)
    if "ERROR" in resp:
        print("MQTT-Stack konnte nicht gestartet werden. Abbruch.")
        ser.close()
        return
    print("MQTT-Stack wurde gestartet!")

    # Rest wie gewohnt
    send_at(ser, f'AT+CMQTTACCQ=0,"{MQTT_client}"')
    send_at(ser, f'AT+CMQTTCONNECT=0,"tcp://{MQTT_server}:{MQTT_port}",60,1,"{MQTT_user}","{MQTT_password}"', timeout=5)
    send_at(ser, f'AT+CMQTTTOPIC=0,{len(MQTT_topic)}')
    ser.write(MQTT_topic.encode())
    time.sleep(1)
    send_at(ser, f'AT+CMQTTMSG=0,{len(MQTT_msg)}')
    ser.write(MQTT_msg.encode())
    time.sleep(1)
    send_at(ser, "AT+CMQTTPUB=0,1,60", timeout=3)
    send_at(ser, "AT+CMQTTDISCONN=0")
    send_at(ser, "AT+CMQTTSTOP")
    ser.close()
    print("Fertig.")

if __name__ == "__main__":
    main()

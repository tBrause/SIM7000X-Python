import serial
import time

def send_at_command(ser, command, timeout=1):
    ser.write((command + '\r\n').encode())
    time.sleep(timeout)
    response = ser.read(ser.inWaiting()).decode()
    print(f"Antwort: {command}\n{response}")
    return response

def main():
    ser = serial.Serial("/dev/ttyS0", 9600)
    ser.flushInput()

    try:
        # Überprüfen der Firmware-Version
        print("\n# Überprüfen der Firmware-Version:")
        send_at_command(ser, "AT+CGMR")

        # Überprüfen des Status der SIM-Karte
        print("\n# Überprüfen des Status der SIM-Karte:")
        send_at_command(ser, "AT+CPIN?")

        # Überprüfen der Netzverbindung
        print("\n# Überprüfen der Netzverbindung:")
        send_at_command(ser, "AT+CREG?")

        # 1. Status der SIM-Karte
        print("\n# Status der SIM-Karte:")
        send_at_command(ser, "AT+CPIN?")

        # 2. Aktiviere MQTT
        print("\n# Aktiviere MQTT")
        send_at_command(ser, "AT+CMQTTSTART")
        send_at_command(ser, f"AT+CMQTTACCQ=0,0,\"{MQTT_SERVER}\"")
        send_at_command(ser, f"AT+CMQTTCONNECT=0,\"tcp://{MQTT_SERVER}:{MQTT_PORT}\",60,1")
        send_at_command(ser, f"AT+CMQTTSUB=0,1,\"{MQTT_TOPIC}\",1")
        send_at_command(ser, f"AT+CMQTTTOPIC=0,0,\"{MQTT_TOPIC}\"")
        send_at_command(ser, f"AT+CMQTTPAYLOAD=0,0,\"{MQTT_MESSAGE}\"")
        send_at_command(ser, f"AT+CMQTTPUB=0,1,60")
        
    finally:
        # Schließe die serielle Verbindung
        ser.close()
        print("# Serielle Verbindung geschlossen.\n")

# Skript starten
if __name__ == "__main__":
    main()
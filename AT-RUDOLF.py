import serial
import time

def send_at_command(ser, command, expected_response, timeout=2):
    ser.write((command + '\r').encode())
    time.sleep(timeout)
    response = ser.read(ser.in_waiting).decode()
    if expected_response not in response:
        raise Exception(f"Failed to execute {command}. Response: {response}")
    return response

def main():
    ser = serial.Serial('/dev/serial0', 9600, timeout=1)
    
    try:
        response = send_at_command(ser, 'AT', 'OK')
        print(f"AT response: {response}")
        
        # Überprüfen des Status der SIM-Karte
        print("\n# Überprüfen des Status der SIM-Karte:")
        send_at_command(ser, "AT+CPIN?", "READY")
        
        # Überprüfen der Netzverbindung
        print("\n# Überprüfen der Netzverbindung:")
        send_at_command(ser, "AT+CREG?", "0,1")
        
        # Setze den APN
        print("\n# Setze den APN:")
        send_at_command(ser, 'AT+CGDCONT=1,"IP","internet"', "OK")
        
        response = send_at_command(ser, 'AT+CMEE=2', 'OK')
        print(f"AT+CMEE response: {response}")
        
        response = send_at_command(ser, 'AT+CNMP=38', 'OK')
        print(f"AT+CNMP response: {response}")
        
        # Check signal quality
        while True:
            response = send_at_command(ser, 'AT+CSQ', '+CSQ:')
            csq = int(response.split(':')[1].split(',')[0].strip())
            print(f"AT+CSQ response: {response}, CSQ: {csq}")
            if csq < 99:
                break
            time.sleep(1)
        
        send_at_command(ser, 'AT+COPS?', 'OK')
        send_at_command(ser, 'AT+CNACT=1,"internet"', 'OK')
        send_at_command(ser, 'AT+CGATT?', 'OK')
        
        # Configure MQTT
        send_at_command(ser, 'AT+SMCONF="URL","emqx.energywan.de","1883"', 'OK')
        send_at_command(ser, 'AT+SMCONF="TOPIC","energywan/laboratory"', 'OK')
        send_at_command(ser, 'AT+SMCONF="USERNAME","Labortory"', 'OK')
        send_at_command(ser, 'AT+SMCONF="PASSWORD","Uc6RncyxfyPeH4w"', 'OK')
        send_at_command(ser, 'AT+SMCONF="CLIENTID","EnWAN109973"', 'OK')
        send_at_command(ser, 'AT+SMCONF="QOS","1"', 'OK')
        
        # Check MQTT state
        while True:
            response = send_at_command(ser, 'AT+SMSTATE?', 'OK')
            if '+APP PDP: ACTIVE' in response:
                break
            time.sleep(1)
        
        # Connect to MQTT broker
        send_at_command(ser, 'AT+SMCONN', 'OK')
        send_at_command(ser, 'AT+SMSTATE?', 'OK')
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        ser.close()

if __name__ == "__main__":
    main()
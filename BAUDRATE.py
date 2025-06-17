import serial
import time

# Passe den Port ggf. an!
port = "/dev/serial0"

for baud in [9600, 19200, 38400, 57600, 115200]:
    print(f"Teste Baudrate: {baud}")
    try:
        ser = serial.Serial(port, baud, timeout=1)
        ser.write(b'AT\r\n')
        time.sleep(0.5)
        resp = ser.read(100)
        print(resp)
        if b'OK' in resp:
            print(f"Erfolg mit Baudrate {baud}")
            break
        ser.close()
    except Exception as e:
        print(e)

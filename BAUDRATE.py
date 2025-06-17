ports = ["/dev/serial0", "/dev/ttyS0", "/dev/ttyAMA0"]
for port in ports:
    print(f"Teste Port: {port}")
    for baud in [9600, 19200, 38400, 57600, 115200]:
        try:
            print(f"  Teste Baudrate: {baud}")
            ser = serial.Serial(port, baud, timeout=1)
            ser.write(b'AT\r\n')
            resp = ser.read(100)
            print(f"  Antwort: {resp}")
            ser.close()
        except Exception as e:
            print(f"  Fehler: {e}")

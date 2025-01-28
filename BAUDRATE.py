import serial

SERIAL_PORT = "/dev/serial0"
BAUD_RATE = 9600

def is_port_in_use_and_correct_baudrate(port, baudrate):
    """Prüft, ob der serielle Port frei ist und ob die Baudrate funktioniert."""
    try:
        ser = serial.Serial(port, baudrate=baudrate, timeout=1)
        ser.write(b'AT\r')  # Testbefehl senden (z. B. AT)
        response = ser.read(64)  # Antwort lesen
        ser.close()  # Sofort schließen
        if response.strip():
            return (False, True)  # Port ist frei und Baudrate passt
        else:
            return (False, False)  # Port ist frei, aber keine Antwort
    except serial.SerialException:
        return (True, False)  # Port ist belegt

# Prüfen
is_in_use, is_baudrate_correct = is_port_in_use_and_correct_baudrate(SERIAL_PORT, BAUD_RATE)

if is_in_use:
    print(f"Fehler: Der serielle Port {SERIAL_PORT} ist bereits belegt!")
elif not is_baudrate_correct:
    print(f"Fehler: Der serielle Port {SERIAL_PORT} ist frei, aber keine Antwort mit Baudrate {BAUD_RATE}.")
else:
    print(f"Der serielle Port {SERIAL_PORT} ist frei und die Baudrate {BAUD_RATE} funktioniert!")

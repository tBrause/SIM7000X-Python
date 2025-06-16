import serial
import serial.tools.list_ports

SERIAL_PORT = "/dev/serial0"

def is_port_in_use(port):
    """Prüft, ob der serielle Port bereits belegt ist."""
    try:
        ser = serial.Serial(port, timeout=1)
        ser.close()  # Sofort schließen, wenn erfolgreich geöffnet
        return False  # Port ist nicht belegt
    except serial.SerialException:
        return True  # Port ist belegt

if is_port_in_use(SERIAL_PORT):
    print(f"Fehler: Der serielle Port {SERIAL_PORT} ist bereits belegt!")
else:
    print(f"Der serielle Port {SERIAL_PORT} ist frei und kann verwendet werden.")
    # Hier kannst du deine eigentliche Logik einfügen

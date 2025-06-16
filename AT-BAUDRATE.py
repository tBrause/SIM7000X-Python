import serial

SERIAL_PORT = "/pi/serial0"
TEST_BAUDRATES = [9600, 19200, 38400, 57600, 115200]  # Baudraten zum Testen
TEST_COMMAND = b"AT\r"  # Beispielbefehl für SIM7000 oder NB-IoT
EXPECTED_RESPONSE = b"OK"  # Typische Antwort auf "AT"

def test_baudrates(port, baudrates, test_command, expected_response):
    for baudrate in baudrates:
        try:
            print(f"Teste Baudrate: {baudrate}...")
            with serial.Serial(port, baudrate, timeout=1) as ser:
                ser.write(test_command)  # Testbefehl senden
                response = ser.read(64)  # Antwort lesen
                if expected_response in response:
                    print(f"Erfolg: Baudrate {baudrate} funktioniert!")
                    return baudrate
                else:
                    print(f"Keine Antwort oder unerwartete Antwort bei Baudrate {baudrate}.")
        except serial.SerialException as e:
            print(f"Fehler bei Baudrate {baudrate}: {e}")
    return None

# Baudrate testen
working_baudrate = test_baudrates(SERIAL_PORT, TEST_BAUDRATES, TEST_COMMAND, EXPECTED_RESPONSE)

if working_baudrate:
    print(f"Kommunikation erfolgreich mit Baudrate: {working_baudrate}")
else:
    print("Keine Baudrate hat funktioniert.")

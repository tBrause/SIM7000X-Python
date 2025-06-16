import serial
import time

def send_at_command(command, ser):
    ser.write((command + '\r\n').encode())
    time.sleep(1)
    response = ser.read_all().decode()
    return response

def main():
    # Open serial port
    ser = serial.Serial('/dev/serial0', baudrate=9600, timeout=1)
    
    # Power on GNSS
    response = send_at_command('AT+CGNSPWR=1', ser)
    print("Power on GNSS response:", response)
    
    # Wait for GNSS to power up
    time.sleep(2)
    
    # Get GNSS information
    response = send_at_command('AT+CGNSINF', ser)
    print("GNSS information response:", response)
    
    # End GNSS session
    response = send_at_command('AT+CGNSPWR=0', ser)
    print("End GNSS session response:", response)
    
    
    # Close serial port
    ser.close()

if __name__ == "__main__":
    main()
import serial, time

ser = serial.Serial("/dev/serial0", 115200, timeout=1)
time.sleep(1)
def at(cmd, t=1):
    ser.write((cmd+"\r\n").encode()); time.sleep(t)
    resp = ser.read_all().decode(errors='ignore')
    print(f"-->{cmd}\n<--{resp.strip()}")
    return resp

at("AT")
at('AT+CGDCONT=1,"IP","lpwa.vodafone.com"')
# keine Kontext-Bausteine, wie in deinem funktionierenden Code
#at('AT+SMCONF="URL","tcp://emqx.c2.energywan.de:1883"')
at('AT+SMCONF="URL","tcp://test.mosquitto.org:1883"')
at(f'AT+SMCONF="USERNAME","sww_ZL6xVtWQjN"')
at(f'AT+SMCONF="PASSWORD","sukFYfDzvrnsy8hD"')
at(f'AT+SMCONF="CLIENTID","TOMTEST01"')
at("AT+CGPADDR")
at("AT+CGPSTATUS")

at("AT+SMCONN")
time.sleep(2)

at("AT+SMSTATE?")
at("AT+SMSTAT?")

at(f'AT+SMPUB="hello",0,60')
# ggf. Daten payload direkt danach
time.sleep(1)
at("AT+SMDISC")
time.sleep(1)
at('AT+SMSTATE?')
at('AT+SMSTAT?')
at('AT+SMERROR?')
ser.close()

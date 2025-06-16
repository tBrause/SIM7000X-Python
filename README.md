# SIM7000X-Python

# Vorbereitungen

## Seriellen Port aktivieren

```
sudo raspi-config
```

> Wechsle zu: `3. Interface Options`

> Wechsle zu: `I6 Serial Port`

> Would you like a login shell to be accessible over serial? : `NO`

> Would you like the serial port hardware to be enabled? : `YES`

> Infofenster: `OK`

> Wechsle zu: `FINISH`

> Would you like reboot now? : `YES`

## Python 3

```
python --version
```

> Wenn Python 3 nicht installiert ist

```
sudo apt update
```

```
sudo apt install python3
```

## Bibliotheken

```
sudo apt update
```

```
sudo apt install python3-serial python3-rpi.gpio
```

## Kommunikation als User

```
sudo usermod -a -G dialout $USER
```

```
newgrp dialout
```

```
sudo reboot
```

## Scripte

### Ausführbar machen

```
chmod +x *.py
```

### Erste Zeile aller Python Scripte

```
#!/usr/bin/env python3
```

### Seriellen Port anpassen

```
SERIAL_PORT = "/dev/serial0"
```

---

## Allgemeine Tests

### Serieller Port

> Prüft, ob der serielle Port bereits belegt ist.

```
python PORT.py
```

### Finde serielle Ports und Baudraten für SIM7000X

> Findet alle seriellen Ports und Baudraten, die für den SIM7000X geeignet sind.

```
python AT-BAUDRATE.py
```

### Serieller Port mit Baudrate 9600

> Prüft, ob der serielle Port frei ist und ob die Baudrate 9600 funktioniert.

```
python BAUDRATE.py
```

## Spezifische Tests

### SIM-Karte

> Verschiedene Test und Informationen über die SIM-Karte.

```
python AT-SIM.py
```

### TCP Verbindung

> Testet die TCP-Verbindung.

```
python AT-TCP.py
```

### GPIO Verbindung

> Testet die GPIO-Verbindung und sendet den AT Befehl: AT.

```
python AT-GPIO.py
```
---

## Serieller Port

* **Zeige serielle Ports**

```
ls /dev/serial*
```

* **Prüfe, ob der Port existiert**

```
ls -l /dev/serial0
```

* **Prüfe Prozesse serial0**

```
ps aux | grep serial0
```

## minicom

> Das ist das Werkzeug für das Verwenden von AT Befehlen

```
sudo apt update
```

```
sudo apt install minicom
```

> Zugriff über minicom zu /dev/serial0

```
minicom -D /dev/serial0 -b 9600
```

## SIM Card

* **Status der SIM Karte**

> Ergebnis sollte sein: +CPIN: READY

```
AT+CPIN?
```
> Mögliche Resultate

* +CPIN: SIM PIN → SIM benötigt eine PIN.
* +CPIN: SIM PUK → SIM ist gesperrt und benötigt den PUK.
* +CPIN: READY → SIM ist entsperrt und bereit.

---

* **Ist die Karte eingelegt?**

> Ergebnis sollte sein: +CSMINS: 0,1

```
AT+CSMINS?
```

> Mögliche Resultate

* +CSMINS: 0,1 → SIM ist eingelegt.
* +CSMINS: 0,0 → SIM wird nicht erkannt (möglicherweise ein physisches Problem).

--- 

* **Zeige den aktuellen Netzbetreiber**

```
AT+COPS?
```

* **Signal Quality Report**

```
AT+CSQ
```

---

### MQTT

> MQTT-Verbindung aktivieren

```
AT+CMQTTSTART
```

> MQTT-Broker konfigurieren

```
AT+CMQTTACCQ=0,"client_id"
```

```
AT+CMQTTCONNECT=0,"tcp://broker.hivemq.com:1883",60,1
```

> Trenne die MQTT-Verbindung

```
AT+CMQTTDISC=0,60
```

> MQTT deaktivieren

```
AT+CMQTTSTOP
```

---

### HTTP

* **Besteht eine HTTP Verbindung?**
* Ergebnis sollte sein: OK

```
AT+HTTPPARA="URL","https://httpbin.org/get"
```

* **Bei ERROR**

> aktiviere den HTTP-Service

```
AT+HTTPINIT
```

> Status

```
AT+HTTPSTATUS
```

> Andere Abfragen

1. HTTP-GET-Anfrage senden

```
AT+HTTPACTION=0
```

2. Ergebnis überprüfen

```
AT+HTTPREAD
```

> HTTP Service beenden

```
AT+HTTPTERM
```

---

## GPS

* **GNSS-Modul einschalten**

```
AT+CGNSPWR=1
```

* **Aktuelle GNSS-Daten auslesen**

> Ergebnis sollte sein: +CGNSINF: 1,1,20250117,52.520008,13.404954,34.0,0.0,0.0,0.89

```
AT+CGNSINF
```

> Mögliche Resultate

* GNSS_Status: 1 bedeutet GNSS ist aktiviert.
* Fix_Status: 1 bedeutet, ein gültiger Fix wurde erreicht.
* UTC_Date_Time: Zeitstempel der Position
* Latitude, Longitude: Koordinaten
* Altitude: Höhe in Metern über dem Meeresspiegel.

* **GNSS-Modul ausschalten**

```
AT+CGNSPWR=0
```

---

## Driver / Demo

> 7z installieren

```
sudo apt-get install p7zip-full
```

> In den Downloadordner wechsel

> Demo herunterladen

```
wget https://files.waveshare.com/upload/2/24/SIM7000X-Demo.7z
```

> Entpacken

```
7z x SIM7000X-Demo.7z -r -o/home/pi/SIM7000-Demo
```

> Rechte ändern

```
sudo chmod 777 -R /home/pi/SIM7000-Demo
```

> Es funktioniert !!!

```
wget https://www.waveshare.com/w/upload/4/42/SIM7X00-Driver.7z
```

> https://www.waveshare.com/w/upload/4/42/SIM7X00-Driver.7z

> https://files.waveshare.com/upload/4/42/SIM7X00-Driver.7z

### Fragen / Infos

> sudo nano /etc/rc.local

> Bisher ist SIM7X00-Driver nicht installiert, aber es geht was???

# AT Befehle

Folgende Typen an Commands gibt es:

* Test Command
* Read Command
* Write Command
* Execution Command

## Test & Read Commands

> Test Commands enden meist mit: =?

### Test Commannds

> Verbindung zwischen Hardware und dem HAT testen

```
AT
```

> Sends an IPv6 ping

```
AT+SNPING6=?
```

> Request Manufacturer Identification

```
AT+GMI=?
```

> Display Product Identification Information

```
AT+GMI
```

> Request TA Model Identification

```
AT+GMM=?
```

> Request TA Revision Identification of Software Release

```
AT+GMR
```

> Check GPIO

```
AT+SGPIO
```

> Request TA Revision Identification of Software Release

```
AT+GMR
```

> Request Global Object Identification

```
AT+GOI=?
```

> TE-TA Control Character Framing

```
AT+ICF=?
```

> TE-TA Fixed Local Rate

```
AT+IPR=?
```

> TA returns a list of quadruplets, each representing an operator present in
the network. Any of the formats may be unavailable and should then be an
empty field. The list of operators shall be in order: home network,
networks referenced in SIM, and other networks. 

```
AT+COPS=?
```

> TA returns an alphanumeric string indicating whether some password is
required or not.

> Check

```
AT+CPIN=?
```

> Read

```
AT+CPIN?
```

> GNSS NMEA Out Frequency Configure

```
AT+CGNSRTMS?
```

> 

```
AT+CASRIP?
```

> 

```
AT+CIPHEAD?
```

> f

```
AT+HTTPPARA?
```

# Produkt

* [waveshare.com](https://www.waveshare.com/sim7000e-nb-iot-hat.htm)

# Dokumentationen

* [Wiki](https://www.waveshare.com/wiki/SIM7000E_NB-IoT_HAT)
* [SIM7000E-NB-IoT-HAT-Manual-EN](https://www.waveshare.com/w/upload/7/76/SIM7000E-NB-IoT-HAT-Manual-EN.pdf)
* [SIM7000_Series_AT_Command_Manual](https://files.waveshare.com/upload/3/3c/SIM7000_Series_AT_Command_Manual_V1.05.pdf)
* [SIM7000_Series_HTTP_Application_Note](https://files.waveshare.com/upload/5/57/SIM7000_Series_HTTP_Application_Note_V1.01.pdf)
* [SIM7000_Series_MQTT_Application_Note](https://files.waveshare.com/upload/d/d0/SIM7000_Series_MQTT_Application_Note_V1.00.pdf)
* [SIM7000_Series_SSL_Application_Note](https://www.waveshare.com/w/upload/a/a8/SIM7000_Series_SSL_Application_Note_V1.00.pdf)

# Tutorials

* [Youtube Playlist](https://www.youtube.com/watch?v=l3He0RGahN4&list=PLgaBn0jQyAtIMUsLOufd66ymv0PCxH08j)
* [Testing Raspberry Pi + SIM7000E NB-IoT HAT](https://cytrontechnologies.github.io/maxis-nbiot-hackathon/raspberrypi/nbiot/)

# Github

* [sim7000-tools](https://github.com/tmcadam/sim7000-tools/tree/master)

# Tools

* [SSCOM](https://www.waveshare.com/wiki/File:Sscom.7z)
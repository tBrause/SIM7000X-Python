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

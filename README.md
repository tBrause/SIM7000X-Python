# SIM7000X-Python

# Vorbereitungen

## raspi-config

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

## Autostart

### Entferne: console=serial0,115200

```
sudo nano /boot/firmware/cmdline.txt
```

```
sudo systemctl disable serial-getty@serial0.service
sudo systemctl stop serial-getty@serial0.service
```

```
sudo reboot
```

## Serielle Ports mit socat in mehrere Instanzen aufteilen

```
sudo apt update
```

```
sudo apt install socat
```

> SIM7000X HAT soll `/dev/virtual_serial0` nutzen

```
sudo socat -d -d pty,link=/dev/virtual_serial0,raw tcp:localhost:9000 &
```

## Scripte

## Ausführbar machen

```
chmod +x *.py
```

## Erste Zeile aller Python Scripte

```
#!/usr/bin/env python3
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

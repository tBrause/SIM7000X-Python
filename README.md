# SIM7000X-Python

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

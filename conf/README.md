# Installation

- Wechsel in das Verzeichnis

```
cd /home/pi/EnergyWAN/config
```

- Erstelle die confBatt.json

```
nano confBatt.json
```

- Füge den Inhalt ein

> **Alle Werte sind Beispiele und müssen angepasst werden!**

```
{
  "#Comment":"Battery configuration",
  "eta1":{"cid":602,"et":2},
  "eta2":{"cid":602,"et":2},
  "eta3":{"cid":602,"et":2},
}
```

- Erstelle die confDevice.json

```
nano confDevice.json
```

- Füge den Inhalt ein

> **DEVIVENO: Laufende Nummer des Devices / Bootes unbedingt ändern!**

> **Alle weiteren Werte sind Beispiele und müssen angepasst werden!**

```
{
  "#Comment":"Device configuration",
  "PROVAPN":"web.vodafone.de",
  "PROVOPS":"26202",
  "SIMPIN":"6442"
  "URL":"emqx.energywan.de;1883",
  "USERNAME":"Labortory",
  "PASSWORD":"Uc6RncyxfyPeH4w",
  "TOPIC":"energywan/laboratory",
  "DEVICEID":"energywan/laboratory"
  "CLIENTID":"EnWAN10997",
  "DEVICENO":"3"
}
```

- Überprüfe die Rechte und Eigentümer der Dateien

```
ls -l
```

# Konfiguration

## Konfiguration für das Batterie-System

### Datei: confBatt.json

#### Inhalt (formal):

```
{
  "#Comment":"Battery configuration",
  "etax":{"cid":602,"et":y},
}
```

> Für jedes EMSC(etax) existiert ein JSON-Paar mit...  
>  x = Laufenden Nummer 1..  
>  y = Anzahl angedockter PowerCubes (et)

---

## Configuration der Anwendung

### Datei: confDevice.json

#### Inhalt (im Beispiel für Vodsfone ...)

```
{
  "#Comment":"Device configuration",
  "PROVAPN":"web.vodafone.de",
  "PROVOPS":"26202",
  "SIMPIN":"6442"
  "URL":"emqx.energywan.de;1883",
  "USERNAME":"Labortory",
  "PASSWORD":"Uc6RncyxfyPeH4w",
  "TOPIC":"energywan/laboratory",
  "DEVICEID":"energywan/laboratory"
  "CLIENTID":"EnWAN10997",
  "DEVICENO":"3"
}
```

#### Bedeutung der Paare "key":"value"

- PROVAPN: Access Point Name des Providers
- PROVOPS: Numerischer Wert zur Kennzeichnung des Providers  
  Bekannt: Telekom="26201", Vodafone="26202",E-Plus="26203"
- SIMPIN: PIN der SIM-Karte (wenn erforderlich)
- URL: Adresse und Port des Brokers
- USERNAME: Benutzername (wenn notwendig)
- PASSWORD: Passwort (wenn notwendig)
- TOPIC: MQTT-Topic
- DEVICEID: MQTT-Identifier
- CLIENTID: Vom Broker akzeptierter ClientID
- DEVIVENO: Laufende Nummer des Devices / Bootes
  === Die laufende Nummer muss für jedes Device / Boot
  unterschiedlich sein!! ====

* Die "DEVIVENO" wird als String an "DEVIVEID" und "CLIENTID" angehängt, damit
  sind diese Werte pro Device / Boot eindeutig.

#### Beispiele:

> 1. Beispiel:

- "DEVICENO":"8" -> "DEVICEID":"energywan/laboratory8"
- "CLIENTID":"EnWAN109978"

> 2. Beispiel:

- "DEVICENO":"12" -> "DEVICEID":"energywan/laboratory12"
- "CLIENTID":"EnWAN1099712"

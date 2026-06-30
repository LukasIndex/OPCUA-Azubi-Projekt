# OPCUA-Azubi-Projekt

## Projektbeschreibung
Dieses Projekt implementiert einen OPC UA Client in Python, der über die Kommandozeile gesteuert wird. Der Client unterstützt:

- einmaliges Auslesen von OPC UA Werten (Read)
- kontinuierliches Abonnieren von Werten (Subscribe)
- Event-Subscriptions mit Auswertung von Alarm- und Statusmeldungen
- interaktive Eingaben oder vollständige Steuerung über Kommandozeilenparameter
- anonymen Zugriff oder Login mit Benutzername und Passwort
- Anzeige der Maschinenbezeichnung, sofern der OPC UA Server diese bereitstellt

Das Projekt eignet sich besonders für Tests, Debugging, Schulungen und den Einsatz auf Embedded-Systemen wie dem Revolution Pi.

Repository:
https://github.com/LukasIndex/OPCUA-Azubi-Projekt.git

## Anforderungen
Für die Nutzung werden folgende Komponenten benötigt:

- Python 3.11 (empfohlen)
- pip als Paketmanager
- virtuelle Umgebung (venv)
- die Pakete asyncua und rich

Der verwendete OPC UA Server sollte einen Endpoint wie zum Beispiel opc.tcp://localhost:4840 bereitstellen und mindestens folgende Nodes anbieten:

- ns=2;s=Simulator/Trigonometry/SineValue
- ns=2;s=Simulator/Demo/GroupA/ExampleNode
- ns=2;s=Simulator/Boolean/BoolAlternating

## Installation

### 1. Virtuelle Umgebung anlegen
Unter Windows:

```powershell
python -m venv .venv
.venv\Scripts\activate
```

Unter Linux oder auf dem Revolution Pi:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Abhängigkeiten installieren

```bash
pip install asyncua rich
```

Optional kann das Projekt als Paket installiert werden:

```bash
pip install -e .
```

## Nutzung

### Interaktiver Modus
Das Programm kann interaktiv gestartet werden und fragt alle nötigen Eingaben ab:

```bash
opcua-client --interactive
```

Beispielablauf:

```text
Starte OPC UA Client
Server Adresse eingeben: opc.tcp://localhost:4840
Benutzername eingeben (ENTER = anonym):
Gib dein Passwort ein:
Abfrage Wert eingeben: ns=2;s=Simulator/Trigonometry/SineValue
Read oder Subscribe? (R/s):
```

### Kommandozeilenmodus
Das Programm kann vollständig über Parameter gesteuert werden.

#### Read

```bash
opcua-client --server opc.tcp://localhost:4840 --node "ns=2;s=Simulator/Demo/GroupA/ExampleNode" --mode read
```

#### Subscribe

```bash
opcua-client --server opc.tcp://localhost:4840 --node "ns=2;s=Simulator/Trigonometry/SineValue" --mode subscribe
```

#### Mit Benutzeranmeldung

```bash
opcua-client --server opc.tcp://localhost:4840 --node "ns=2;s=Simulator/Trigonometry/SineValue" --username operator --password operator123 --mode subscribe
```

#### Events anzeigen

```bash
opcua-client --server opc.tcp://localhost:4840 --event --interactive
```

## Parameterübersicht

- -s, --server → OPC UA Endpoint
- -u, --username → Benutzername
- -p, --password → Passwort
- -i, --interactive → Aktiviert interaktiven Modus
- -e, --event → Aktiviert Event-Subscriptions
- -n, --node → NodeId
- -m, --mode → read oder subscribe (read ist Fallback)

## Beispielausgaben

### Read

```text
Starte OPC UA Client
Angemeldet als: admin
Maschinen Bezeichnung: DemoServer
Node: ns=2;s=Simulator/Demo/GroupA/ExampleNode
Wert gelesen: 3.27
```

### Subscribe

```text
Starte OPC UA Client
Angemeldet als: admin
Subscription startet gleich...
Subscription läuft... (STRG+C zum Beenden)
0.12
0.78
1.45
```

### Events

```text
Event Subscription startet...
Events laufen... (STRG+C zum Beenden)
Event: Alarm ausgelöst | Severity: 800
```

## Projektstruktur

- src/opcua_client/main.py enthält den Programmeinstieg und die Ablaufsteuerung
- src/opcua_client/opcua_client.py enthält die OPC UA Kommunikation für Read, Subscribe und Events
- src/opcua_client/cli.py enthält die Kommandozeilen- und Eingabe-Logik
- src/opcua_client/config.py enthält zentrale Konfiguration

## Häufige Fehler

- Eine falsche NodeId führt zu Fehlern wie BadNodeIdUnknown. Die NodeId sollte geprüft oder direkt aus UA Expert kopiert werden.
- Ein falsches NodeId-Format führt ebenfalls zu Problemen. Beispiel:
  - Objects/Simulator/... ist falsch
  - ns=2;s=Simulator/... ist richtig
- Ein fehlendes Python-Paket führt zu Fehlern wie ModuleNotFoundError: asyncua oder rich. In diesem Fall hilft:

```bash
pip install asyncua rich
```

oder bei installierter Paketdefinition:

```bash
pip install -e .
```

## Erweiterungsmöglichkeiten
Das Projekt kann erweitert werden um:

- gleichzeitiges Abonnieren mehrerer Nodes
- Logging der Werte in Dateien (CSV oder JSON)
- automatische Wiederverbindung bei Verbindungsverlust
- grafische Darstellung von Messwerten
- Komfortfunktionen wie Node-Auswahlmenüs oder Konfigurationsdateien

## Zusammenfassung
Dieses Projekt bietet einen einfachen und flexiblen Einstieg in die Nutzung von OPC UA mit Python. Es kombiniert eine intuitive Kommandozeilensteuerung mit Funktionen wie Read, Subscribe und Event-Monitoring und eignet sich sowohl für Tests, Debugging und Schulungszwecke als auch für den Einsatz auf Embedded-Systemen.
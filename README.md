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

#### Mit ausführlicher Ausgabe (Verbose-Modus)

```bash
opcua-client --server opc.tcp://localhost:4840 --node "ns=2;s=Simulator/Demo/GroupA/ExampleNode" --mode read --verbose
```

Die Verbose-Option zeigt detaillierte Informationen an:
- Den OPC UA Endpoint
- Die NodeId
- Den gewählten Modus
- Verbindungsstatus
- Debug-Informationen

#### Maschinenidentifikation anzeigen

```bash
opcua-client --server opc.tcp://localhost:4840 --identify --verbose
```

Dies zeigt die vom OPC UA Server bereitgestellte Maschinenbezeichnung an.

#### Events anzeigen

```bash
opcua-client --server opc.tcp://localhost:4840 --event --interactive
```

## Parameterübersicht

### Grundlegende Parameter

- `-s, --server` → OPC UA Endpoint (z.B. opc.tcp://localhost:4840)
- `-u, --username` → Benutzername für die Authentifizierung
- `-p, --password` → Passwort für die Authentifizierung
- `-n, --node` → NodeId zum Auslesen oder Abonnieren (z.B. ns=2;s=Simulator/Trigonometry/SineValue)

### Betriebsmodi

- `-i, --interactive` → Aktiviert den interaktiven Modus mit Eingabeaufforderungen für alle Parameter
- `-e, --event` → Aktiviert Event-Subscriptions zur Anzeige von Alarm- und Statusmeldungen
- `-ID, --identify` → Zeigt die Maschinenbezeichnung vom OPC UA Server an
- `-m, --mode` → Wählt den Betriebsmodus: `read` (Einmalige Abfrage) oder `subscribe` (Kontinuierliche Überwachung). Fallback ist `read`

### Ausgabeoptionen

- `-v, --verbose` → Aktiviert ausführliche Ausgabe mit Debug-Informationen und detaillierten Statusmeldungen

## Beispielausgaben

### Read (Standard-Modus)

```text
Wert gelesen: 3.27
```

### Read (Mit Verbose-Ausgabe)

```text
Starte OPC UA Client
Endpoint: opc.tcp://localhost:4840
Node: ns=2;s=Simulator/Demo/GroupA/ExampleNode
Modus: read
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

### Subscribe (Mit Verbose-Ausgabe)

```text
Starte OPC UA Client
Endpoint: opc.tcp://localhost:4840
Node: ns=2;s=Simulator/Trigonometry/SineValue
Modus: subscribe
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
Event: Status Update | Severity: 200
```

### Interaktiver Modus mit Menü

```text
Starte OPC UA Client
Server Adresse eingeben: opc.tcp://localhost:4840
Benutzername eingeben (ENTER = anonym): 
Gib dein Passwort ein:
Event oder Node abfragen? (e/N): N
Abfrage Wert eingeben: ns=2;s=Simulator/Trigonometry/SineValue
Read oder Subscribe? (R/s): s
Starte OPC UA Client
Modus: subscribe
Subscription läuft... (STRG+C zum Beenden)
0.45
0.89
1.23
Nochmal abfragen? (y/N) oder neustarten (r): y
Event oder Node abfragen? (e/N): e
Event Subscription startet...
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

## Erweiterte Funktionen

### Verbose-Modus (Detaillierte Ausgabe)

Der Verbose-Modus aktiviert sich mit der `-v` oder `--verbose` Option und bietet:

- **Detaillierte Statusmeldungen**: Zeigt jeden Schritt der Verbindung und Abfrage an
- **Debug-Informationen**: Erweiterte Logging-Informationen von asyncua werden angezeigt (normalerweise nur bei Fehlern)
- **Verbindungsdetails**: Der genaue OPC UA Endpoint wird angezeigt
- **Parameter-Bestätigung**: Node, Modus und andere Parameter werden vor der Ausführung angezeigt

**Beispiel:**
```bash
opcua-client --server opc.tcp://localhost:4840 --node "ns=2;s=Simulator/Demo/GroupA/ExampleNode" --mode read --verbose
```

### Interaktives Menü

Wenn das Programm ohne spezifische Parameter gestartet wird oder mit `--interactive`, bietet es ein interaktives Menü:

1. **Wahl zwischen Events oder Node-Abfrage**
   ```
   Event oder Node abfragen? (e/N):
   ```

2. **Mehrfach-Abfragen**
   Nach jeder Operation kann der Benutzer:
   - `y` eingeben → Eine neue Abfrage durchführen
   - `r` eingeben → Das Programm neu starten (alle Parameter zurücksetzen)
   - Beliebig anderes / Enter → Beenden

Diese Funktionalität ermöglicht kontinuierliche Tests und Debugging ohne das Programm neu zu starten.

### Maschinenidentifikation

Mit der `--identify` Option kann die Maschinenbezeichnung des OPC UA Servers abgerufen werden:

```bash
opcua-client --server opc.tcp://localhost:4840 --identify --verbose
```

Dies ist besonders nützlich, um zu überprüfen, ob die richtige Maschine angesprochen wird.

### Logging-Kontrolle

- **Ohne Verbose-Modus**: Nur kritische Fehler von asyncua werden angezeigt
- **Mit Verbose-Modus**: Vollständige Debug-Ausgaben von asyncua werden aktiviert

Dies vereinfacht die Fehlersuche erheblich.

## Praxisbeispiele

### Szenario 1: Schnelle Abfrage eines Wertes

```bash
opcua-client --server opc.tcp://192.168.1.100:4840 --node "ns=2;s=Temperature" --mode read
```

**Ausgabe:**
```
25.5
```

### Szenario 2: Debugging mit ausführlicher Ausgabe

```bash
opcua-client --server opc.tcp://localhost:4840 --node "ns=2;s=Simulator/Demo/GroupA/ExampleNode" --verbose
```

**Ausgabe:**
```
Starte OPC UA Client
Endpoint: opc.tcp://localhost:4840
Node: ns=2;s=Simulator/Demo/GroupA/ExampleNode
Modus: read
Wert gelesen: 3.27
```

### Szenario 3: Kontinuierliche Überwachung mit automatischer Authentifizierung

```bash
opcua-client --server opc.tcp://192.168.1.100:4840 --node "ns=2;s=ProcessValue" --username admin --password pass123 --mode subscribe --verbose
```

### Szenario 4: Interaktives Testing auf dem Revolution Pi

```bash
opcua-client --interactive --verbose
```

Hier wird der Benutzer systematisch durch alle Eingaben geführt und kann mehrfach abfragen, ohne das Programm neu zu starten.

### Szenario 5: Event-Monitoring mit Detailausgabe

```bash
opcua-client --server opc.tcp://localhost:4840 --event --verbose
```

Dies zeigt alle Alarm- und Statusereignisse mit vollständigen Debug-Informationen an.

### Szenario 6: Maschinenüberprüfung vor Betrieb

```bash
opcua-client --server opc.tcp://192.168.1.100:4840 --identify --verbose
```

Überprüft, ob die richtige Maschine angesprochen wird, bevor weitere Operationen durchgeführt werden.

## Erweiterungsmöglichkeiten

Das Projekt kann erweitert werden um:

- gleichzeitiges Abonnieren mehrerer Nodes
- Logging der Werte in Dateien (CSV oder JSON)
- automatische Wiederverbindung bei Verbindungsverlust
- grafische Darstellung von Messwerten
- Komfortfunktionen wie Node-Auswahlmenüs oder Konfigurationsdateien
- Caching von häufig verwendeten NodeIds
- Export von Event-Logs in strukturierte Formate
- REST-API für externe Anwendungen

## Zusammenfassung
Dieses Projekt bietet einen einfachen und flexiblen Einstieg in die Nutzung von OPC UA mit Python. Es kombiniert eine intuitive Kommandozeilensteuerung mit Funktionen wie Read, Subscribe und Event-Monitoring und eignet sich sowohl für Tests, Debugging und Schulungszwecke als auch für den Einsatz auf Embedded-Systemen.
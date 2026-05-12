# OPCUA-Azubi-Projekt
Projektbeschreibung
Dieses Projekt implementiert einen OPC UA Client in Python, der über die Kommandozeile gesteuert wird.
Der Client ermöglicht:

das einmalige Auslesen von OPC UA Werten (Read)
das kontinuierliche Abonnieren von Werten (Subscribe)
die Verbindung mit Benutzername und Passwort oder anonym
die Steuerung sowohl interaktiv als auch über Kommandozeilenparameter

Das Projekt eignet sich besonders für Tests, Debugging und Schulungszwecke im Bereich OPC UA sowie für den Einsatz auf Embedded Systemen wie dem Revolution Pi.
Das GitHub‑Repository zum Projekt befindet sich unter:
https://github.com/LukasIndex/OPCUA-Azubi-Projekt.git

Anforderungen
Für die Nutzung werden folgende Komponenten benötigt:

Python Version 3.11 (empfohlen)
pip als Paketmanager
virtuelle Umgebung (venv)
Python Paket asyncua

Der verwendete OPC UA Server muss folgende Anforderungen erfüllen:

Bereitstellung eines OPC UA Endpoints (z. B. opc.tcp://localhost:4840)
Unterstützung für Anonymous Zugriff oder Username/Password Login
vorhandene Nodes, zum Beispiel:
ns=2;s=Simulator/Trigonometry/SineValue
ns=2;s=Simulator/Demo/GroupA/ExampleNode
ns=2;s=Simulator/Boolean/BoolAlternating


Installation
Zunächst wird eine virtuelle Umgebung erstellt und aktiviert.
Unter Windows erfolgt die Aktivierung mit:
.venv\Scripts\activate
Unter Linux oder auf dem Revolution Pi erfolgt die Aktivierung mit:
source .venv/bin/activate
Anschließend wird die Abhängigkeit installiert:
pip install asyncua
Optional kann für die spätere Wiederherstellung der Umgebung eine requirements-Datei erstellt werden:
pip freeze > requirements.txt

Installation auf Revolution Pi


Python Version prüfen:
python3 --version


Projekt herunterladen:
git clone https://github.com/LukasIndex/OPCUA-Azubi-Projekt.git
cd OPCUA-Azubi-Projekt


Virtuelle Umgebung erstellen:
python3 -m venv .venv
source .venv/bin/activate


Abhängigkeiten installieren:
pip install asyncua


Programm starten:
python main.py



Verwendung
Interaktiver Modus
Das Programm kann interaktiv gestartet werden, sodass alle Eingaben abgefragt werden.
Beispiel Ablauf:
Starte OPC UA Client
Server Adresse eingeben: opc.tcp://localhost:4840
Benutzername eingeben (ENTER = anonym):
Gib dein Passwort ein:
Abfrage Wert eingeben: ns=2;s=Simulator/Trigonometry/SineValue
Read oder Subscribe? (r/s):

Automatische Nutzung über Kommandozeile
Das Programm kann vollständig über Parameter gesteuert werden.
Beispiel für Subscribe:
python main.py --server opc.tcp://localhost:4840 --node "ns=2;s=Simulator/Trigonometry/SineValue" --mode subscribe
Beispiel für Read:
python main.py --server opc.tcp://localhost:4840 --node "ns=2;s=Simulator/Demo/GroupA/ExampleNode" --mode read
Beispiel mit Benutzeranmeldung:
python main.py --server opc.tcp://localhost:4840 --node "ns=2;s=Simulator/Trigonometry/SineValue" --username operator --password operator123 --mode subscribe

Parameterübersicht
--server → OPC UA Endpoint
--node → NodeId
--username → Benutzername
--password → Passwort
--mode → read oder subscribe

Beispielausgaben
Read
Starte OPC UA Client
Endpoint: opc.tcp://localhost:4840
Verbindung aufgebaut
Node: ns=2;s=Simulator/Demo/GroupA/ExampleNode
Wert gelesen: 3.27

Subscribe
Starte OPC UA Client
Endpoint: opc.tcp://localhost:4840
Verbindung aufgebaut
Node: ns=2;s=Simulator/Trigonometry/SineValue
Subscription läuft...
Neuer Wert empfangen: 0.12
Neuer Wert empfangen: 0.78
Neuer Wert empfangen: 1.45

Projektstruktur
main.py enthält den Programmeinstieg und die Ablaufsteuerung
opcua_client.py enthält die OPC UA Kommunikation (Read und Subscribe)
cli.py enthält die Benutzereingaben
config.py enthält die Konfiguration

Häufige Fehler
Eine falsche NodeId führt zu einem Fehler wie BadNodeIdUnknown.
In diesem Fall sollte die NodeId überprüft oder direkt aus UA Expert kopiert werden.
Ein falsches Format der NodeId führt ebenfalls zu Fehlern.
Beispiel:
Objects/Simulator/... ist falsch
ns=2;s=Simulator/... ist richtig
Ein fehlendes Python Paket führt zu einem Fehler wie ModuleNotFoundError: asyncua.
In diesem Fall hilft: pip install asyncua

Erweiterungsmöglichkeiten
Das Projekt kann erweitert werden um:

gleichzeitiges Abonnieren mehrerer Nodes
Logging der Werte in Dateien (CSV oder JSON)
automatische Wiederverbindung bei Verbindungsverlust
grafische Darstellung von Messwerten
Komfortfunktionen wie Node-Auswahlmenüs


Zusammenfassung
Dieses Projekt bietet einen einfachen und flexiblen Einstieg in die Nutzung von OPC UA mit Python. Es kombiniert eine intuitive Kommandozeilensteuerung mit leistungsfähigen Funktionen wie Read und Subscribe und ist sowohl für Test- als auch Lernzwecke geeignet.
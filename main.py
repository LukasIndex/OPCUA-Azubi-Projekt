import asyncio
# Importiert das asyncio-Modul, das für asynchrone Programmierung in Python genutzt wird

from config import OPCUA_ENDPOINT, NODE_TO_READ
# Importiert die Konfigurationswerte:
# - OPCUA_ENDPOINT: die Adresse des OPC-UA-Servers
# - NODE_TO_READ: die Node-ID, die gelesen werden soll

from opcua_client import OpcUaClient
# Importiert die selbst geschriebene Klasse OpcUaClient aus der Datei opcua_client.py


async def main():
    # Definition der asynchronen Hauptfunktion

    print("Starte OPC UA Client")
    # Gibt aus, dass das Programm gestartet ist

    print("Endpoint:", OPCUA_ENDPOINT)
    # Gibt den verwendeten OPC-UA-Endpunkt aus

    print("Node:", NODE_TO_READ)
    # Gibt die Node-ID aus, die gelesen wird

    client = OpcUaClient(OPCUA_ENDPOINT)
    # Erstellt ein neues OpcUaClient-Objekt mit dem angegebenen Endpoint

    try:
        # Start eines try-Blocks, um Fehler abzufangen

        await client.connect()
        # Baut asynchron eine Verbindung zum OPC-UA-Server auf

        print("Verbindung aufgebaut")
        # Meldung, dass die Verbindung erfolgreich war

        value = await client.read_node(NODE_TO_READ)
        # Liest asynchron den Wert der angegebenen Node vom Server

        print(f"Wert gelesen: {value}")
        # Gibt den gelesenen Wert aus

    except Exception as e:
        # Fängt alle auftretenden Fehler ab

        print("Fehler:", e)
        # Gibt die Fehlermeldung aus

    finally:
        # Dieser Block wird immer ausgeführt (auch bei Fehlern)

        await client.disconnect()
        # Trennt die Verbindung zum OPC-UA-Server sauber

        print("Client beendet")
        # Meldung, dass der Client beendet wurde


if __name__ == "__main__":
    # Prüft, ob das Skript direkt ausgeführt wird (nicht importiert)

    asyncio.run(main())
    # Startet die asynchrone main()-Funktion über die Event-Loop von asyncio
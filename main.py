import asyncio
import config
from cli import abfrage_wert
from opcua_client import OpcUaClient


async def main():
    
    #---------------------------------------------- Abfrage CLI! --------------------------------------------------

    config.NODE_TO_READ = abfrage_wert()

    print("Starte OPC UA Client")
    print("Endpoint:", config.OPCUA_ENDPOINT)
    print("Node:", config.NODE_TO_READ)

    client = OpcUaClient(config.OPCUA_ENDPOINT)

    try:
        await client.connect()
        print("Verbindung aufgebaut")

        value = await client.read_node(config.NODE_TO_READ)
        print(f"Wert gelesen: {value}")

    except Exception as e:
        print("Fehler:", e)

    finally:
        await client.disconnect()
        print("Client beendet")


if __name__ == "__main__":
    asyncio.run(main())
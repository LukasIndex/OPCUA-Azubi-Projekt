import asyncio
import config
from cli import abfrage_wert, abfrage_pw
from opcua_client import OpcUaClient


async def main():
    print("Starte OPC UA Client")
    print("Endpoint:", config.OPCUA_ENDPOINT)

    password = abfrage_pw()

    client = OpcUaClient(
        config.OPCUA_ENDPOINT,
        username="operator",
        password=password
    )

    try:
        await client.connect()
        print("Verbindung aufgebaut")

        while True:
            config.NODE_TO_READ = abfrage_wert()
            print("Node:", config.NODE_TO_READ)

            value = await client.read_node(config.NODE_TO_READ)
            print(f"Wert gelesen: {value}")

            weiter = input("Nochmal abfragen? (y/n): ").strip().lower()
            if weiter != "y":
                break

    except Exception as e:
        print("Fehler:", e)

    finally:
        await client.disconnect()
        print("Client beendet")


if __name__ == "__main__":
    asyncio.run(main())
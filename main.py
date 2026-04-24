import asyncio
from config import OPCUA_ENDPOINT, NODE_TO_READ
from opcua_client import OpcUaClient

async def main():
    client = OpcUaClient(OPCUA_ENDPOINT)
import asyncio
from config import OPCUA_ENDPOINT, NODE_TO_READ
from opcua_client import OpcUaClient


async def main():
    print("Starte OPC UA Client")
    print("Endpoint:", OPCUA_ENDPOINT)
    print("Node:", NODE_TO_READ)

    client = OpcUaClient(OPCUA_ENDPOINT)

    try:
        await client.connect()
        print("Verbindung aufgebaut")

        value = await client.read_node(NODE_TO_READ)
        print(f"Wert gelesen: {value}")

    except Exception as e:
        print("Fehler:", e)

    finally:
        await client.disconnect()
        print("Client beendet")


if __name__ == "__main__":
    asyncio.run(main())
from asyncua import Client
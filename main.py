import asyncio
from config import OPCUA_ENDPOINT, NODE_TO_READ
from opcua_client import OpcUaClient

async def main():
    client = OpcUaClient(OPCUA_ENDPOINT)

    try:
        await client.connect()
        value = await client.read_node(NODE_TO_READ)
        print(f"Wert von {NODE_TO_READ}: {value}")
    finally:
        await client.disconnect()

if __name__ == "__main__":
    asyncio.run(main())

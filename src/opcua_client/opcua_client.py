import asyncio
from asyncua import Client


class SubscriptionHandler:
    def datachange_notification(self, node, val, data):
        print(f"Neuer Wert empfangen: {val}")


class OpcUaClient:
    def __init__(self, endpoint: str, username: str, password: str):
        self.client = Client(url=endpoint)

       
        if username:
            self.client.set_user(username)

        if password:
            self.client.set_password(password)

    async def connect(self):
        await self.client.connect()

    async def disconnect(self):
        await self.client.disconnect()

    async def read_node(self, node_id: str):
        node = self.client.get_node(node_id)
        return await node.read_value()

    async def subscribe_node(self, node_id: str):
        handler = SubscriptionHandler()

        print("Subscription startet gleich...")
        await asyncio.sleep(0.3)

        subscription = await self.client.create_subscription(500, handler)
        node = self.client.get_node(node_id)

        await subscription.subscribe_data_change(node)

        print("Subscription läuft... (STRG+C zum Beenden)")

        while True:
            await asyncio.sleep(1)

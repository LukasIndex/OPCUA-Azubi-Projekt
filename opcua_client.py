import asyncio
from asyncua import Client


# ✅ Handler für Subscription
class SubscriptionHandler:
    def datachange_notification(self, node, val, data):
        print(f"Neuer Wert empfangen: {val}")


class OpcUaClient:
    def __init__(self, endpoint: str, username: str, password: str):
        self.client = Client(url=endpoint)
        self.client.set_user(username)
        self.client.set_password(password)

    async def connect(self):
        await self.client.connect()

    async def disconnect(self):
        await self.client.disconnect()

    async def read_node(self, node_id: str):
        node = self.client.get_node(node_id)
        return await node.read_value()

    # ✅ NEU: Subscribe Funktion
    async def subscribe_node(self, node_id: str):
        handler = SubscriptionHandler()

        subscription = await self.client.create_subscription(500, handler)
        node = self.client.get_node(node_id)

        await subscription.subscribe_data_change(node)

        print("Subscription gestartet... (STRG+C zum Beenden)")

        while True:
            await asyncio.sleep(1)

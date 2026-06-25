import asyncio
from rich import print  # Import rich print for colored cli output
from asyncua import Client


class SubscriptionHandler:
    def datachange_notification(self, node, val, data):
        print(f"{val}")

class EventSubscriptionHandler:
    def __init__(self):
        self.message = None

    def datachange_notification(self, node, val, data):
        node_id = node.nodeid.to_string()

        if node_id == "ns=2;i=18":
            self.message = val

        elif node_id == "ns=2;i=19":
            severity = val

            if self.message is not None:
                if severity >= 800:
                    color = "red"
                elif severity >= 600:
                    color = "#f47f1f"
                elif severity >= 400:
                    color = "#ffb300"
                elif severity >= 200:
                    color = "#4cae4f"
                else:
                    color = "green"

                print(f"[{color}]Event: {self.message} | Severity: {severity}[/{color}]")


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

    async def machine_name(self):
        try:
            machine_name = await self.read_node("ns=0;i=2261")  # reads the node with the machine name (need for improvement)
            print(f"[blue]Maschinen Bezeichnung: {machine_name}[/blue]")
        except Exception as e:
            print(f"Maschinen Bezeichnung nicht lesbar: {e}")

    async def subscribe_events(self):
        handler = EventSubscriptionHandler()

        print("Event Subscription startet...")
        await asyncio.sleep(0.3)

        subscription = await self.client.create_subscription(500, handler)

        msg_node = self.client.get_node("ns=2;i=18")  # directly reads the nodes for events (need for improvement)
        sev_node = self.client.get_node("ns=2;i=19")

        await subscription.subscribe_data_change(msg_node)
        await subscription.subscribe_data_change(sev_node)

        print("Events laufen... (STRG+C zum Beenden)")

        while True:
            await asyncio.sleep(1)

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

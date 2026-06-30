import asyncio
import opcua_client.config as config
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

    async def machine_identifiers(self):
        try:
            machine_name = await self.read_node(config.MACHINE_ID)  # reads the node with the machine name
            build_number = await self.read_node(config.BUILD_NUMBER)
            print(f"[blue]Maschinen Bezeichnung: {machine_name}, Buildnummer: {build_number} [/blue]")
        except Exception as e:
            print(f"Maschinen Identifizierungen nicht lesbar: {e}")

    async def subscribe_events(self):
        handler = EventSubscriptionHandler()

        await asyncio.sleep(0.3)

        subscription = await self.client.create_subscription(500, handler)

        msg_node = self.client.get_node(config.EVENT_MESSAGE)  # directly reads the nodes for events
        sev_node = self.client.get_node(config.EVENT_SEVERITY)

        await subscription.subscribe_data_change(msg_node)
        await subscription.subscribe_data_change(sev_node)

        while True:
            await asyncio.sleep(1)

    async def subscribe_node(self, node_id: str):
        handler = SubscriptionHandler()

        await asyncio.sleep(0.3)

        subscription = await self.client.create_subscription(500, handler)
        node = self.client.get_node(node_id)

        await subscription.subscribe_data_change(node)

        while True:
            await asyncio.sleep(1)

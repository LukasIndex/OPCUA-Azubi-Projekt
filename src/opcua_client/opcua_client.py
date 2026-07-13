import asyncio
import opcua_client.config as config
from asyncua import Client
from rich import print  # Import rich print for colored cli output

class SubscriptionHandler:
    def datachange_notification(self, _node, val, _data):
        print(f"{val}")

class EventSubscriptionHandler:  # handles events
    def event_notification(self, event):
        try:
            self.message = event.Message.Text if hasattr(event, "Message") else "Keine Nachricht"
            severity = event.Severity if hasattr(event, "Severity") else 0

            if severity >= 800:  # give color a value depending on severity
                color = "red"
            elif severity >= 600:
                color = "#f47f1f"
            elif severity >= 400:
                color = "#ffb300"
            elif severity >= 200:
                color = "#4cae4f"
            else:
                color = "green"

            print(f"[{color}]Event: {self.message} | Severity: {severity}[/{color}]")  # prints message in color of severity
        except Exception as e:
            print(f"[red]Fehler bei Events: {e}[/red]")            

class OpcUaClient:  # sets the endpoint, sets the username and password and sets subscription to none
    def __init__(self, endpoint: str, username: str, password: str):
        self.client = Client(url=endpoint)
        self.active_subscription = None

       
        if username:
            self.client.set_user(username)

        if password:
            self.client.set_password(password)

    async def connect(self):  # connect to the server
        await self.client.connect()

    async def disconnect(self):  # disconnect from the server
        await self.client.disconnect()

    async def read_node(self, node_id: str):  # function that reads the specified node from the server
        node = self.client.get_node(node_id)
        return await node.read_value()

    async def machine_identifiers(self): # WONT WORK ON REAL SERVER, reads the nodes specified in config.py
        try:
            machine_name = await self.read_node(config.MACHINE_ID)
            build_number = await self.read_node(config.BUILD_NUMBER)
            print(f"[blue]Maschinen Bezeichnung: {machine_name}, Buildnummer: {build_number} [/blue]")
        except Exception as e:
            print(f"Maschinen Identifizierungen nicht lesbar: {e}")

    async def subscribe_events(self):  # creates event subscription and uses the handler
        handler = EventSubscriptionHandler()
        await asyncio.sleep(0.3)

        self.active_subscription = await self.client.create_subscription(500, handler)
        event_node = self.client.get_node(config.EVENT_NODE)  # get_node to define which node to subscribe
        await self.active_subscription.subscribe_events(event_node)

    async def subscribe_node(self):  # creates node subscription
        handler = SubscriptionHandler()
        await asyncio.sleep(0.3)

        self.active_subscription = await self.client.create_subscription(500, handler)
        node = self.client.get_node(config.NODE_TO_READ)
        await self.active_subscription.subscribe_data_change(node)

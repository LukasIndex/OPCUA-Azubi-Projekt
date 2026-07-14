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

    async def show_nodes(self, node=None, indent=0):  # prints every node that the server has
        if node == None:
            node = self.client.nodes.root

        print(" " * indent + f"-{await node.read_display_name()} ({node.nodeid})")

        children = await node.get_children()
        for child in children:
            await self.show_nodes(child, indent + 4)

    async def read_node(self, node_id: str):  # function that reads the specified node from the server
        node = self.client.get_node(node_id)
        return await node.read_value()

    async def machine_identifiers(self): # reads standart nodes for identification
        try:
            name_node = self.client.get_node("ns=0;i=2261")
            product_name = await name_node.read_value()
            if hasattr(product_name, "Text"): product_name = product_name.Text

            print(f"Produktname: {product_name}")
        except Exception:
            print("Es konnten keine Identifizierungswerte ausgelesen werden")

    async def server_diagnostics(self):  # reads the server status and prints it
        try:
            status_node = self.client.get_node("ns=0;i=2256")
            server_status = await status_node.read_value()
            if hasattr(server_status, "Text"): server_status = server_status.Text
            print(server_status)
        except Exception:
            print("Es konnten keine Diagnosedaten ausgelesen werden")

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

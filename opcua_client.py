from asyncua import Client


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
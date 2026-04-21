from asyncua import Client

class OpcUaClient:
    def __init__(self, endpoint):
        self.endpoint = endpoint
        self.client = Client(url=endpoint)

    async def connect(self):
        await self.client.connect()

    async def disconnect(self):
        await self.client.disconnect()

    async def read_node(self, node_id):
        node = self.client.get_node(node_id)
        return await node.read_value()

    async def write_node(self, node_id, value):
        node = self.client.get_node(node_id)
        await node.write_value(value)
from channels.generic.websocket import AsyncJsonWebsocketConsumer


class EchoConsumer(AsyncJsonWebsocketConsumer):
    async def receive_json(self, content, **kwargs):
        await self.send_json(content)

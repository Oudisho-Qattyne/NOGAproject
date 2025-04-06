from channels.generic.websocket import AsyncWebsocketConsumer

class SourceConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Authenticate the ESP32 (e.g., via query token)
        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        if bytes_data:
            # Broadcast the frame to all viewers
            await self.channel_layer.group_send(
                "video_stream",
                {
                    "type": "video.frame",
                    "data": bytes_data
                }
            )

class ViewerConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Add viewer to the video_stream group
        await self.channel_layer.group_add("video_stream", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("video_stream", self.channel_name)

    async def video_frame(self, event):
        # Send video frame to the viewer
        await self.send(bytes_data=event["data"])
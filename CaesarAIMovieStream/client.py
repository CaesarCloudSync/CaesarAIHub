import asyncio
import websockets
import json

async def send_message():
    uri = "ws://localhost:8082/api/v1/stream_get_gamews"  # Replace with your WebSocket server URI
    async with websockets.connect(uri) as websocket:
        message = {"title": "Shadow of war"}
        await websocket.send(json.dumps(message))
        print(f"Sent: {message}")
        while True:
            try:
                # Wait for a response from the server
                response = await websocket.recv()
                print(response)
                with open("response.json", "a+") as f:
                    f.write(response)
                print(f"Received: {response}")
            except websockets.ConnectionClosed:
                print("Connection closed")
                break

# Run the client
asyncio.run(send_message())

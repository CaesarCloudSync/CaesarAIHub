import asyncio
import aiohttp
import json

STREAM_URL = "http://127.0.0.1:8081/api/v1/stream_get_single_episodes?title=Fullmetal alchemist&season=1&episode=1"  # Change if hosted elsewhere

async def fetch_stream():
    async with aiohttp.ClientSession() as session:
        async with session.get(STREAM_URL) as response:
            buffer = ""
            async for chunk in response.content.iter_any():
                buffer += chunk.decode("utf-8")
                try:
                    data = json.loads(buffer)  # Try parsing JSON
                    print("Received:", data)
                    buffer = ""  # Reset buffer after successful parse
                except json.JSONDecodeError:
                    continue  # Wait for more data if JSON is incomplete

if __name__ == "__main__":
    asyncio.run(fetch_stream())
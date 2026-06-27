import httpx
import asyncio

async def test():
    async with httpx.AsyncClient(timeout=300.0) as client:
        r = await client.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "gemma2:2b",
                "prompt": "say hello",
                "stream": False
            }
        )
        print("Status:", r.status_code)
        print("Response:", r.text[:1000])

asyncio.run(test())
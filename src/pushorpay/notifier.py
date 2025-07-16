import os
import httpx
from dotenv import load_dotenv

"""Handle Discord notification"""

load_dotenv()
DISCORD_WEBHOOK = os.environ["DISCORD_WEBHOOK"]


async def post_to_discord(message: str) -> None:
    async with httpx.AsyncClient() as client:
        await client.post(DISCORD_WEBHOOK, json={"content": message})

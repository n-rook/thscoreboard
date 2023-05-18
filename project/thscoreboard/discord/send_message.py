import os
from discord import Client, Intents

DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
DISCORD_BOT_CHANNEL_ID = os.getenv("DISCORD_BOT_CHANNEL_ID")


def send_discord_message(message: str) -> None:
    client = Client(intents=Intents.default())

    @client.event
    async def on_ready():
        channel = client.get_channel(int(DISCORD_BOT_CHANNEL_ID))
        await channel.send(message)
        await client.close()

    client.run(DISCORD_BOT_TOKEN)


if __name__ == "__main__":
    from dotenv import load_dotenv
    from pathlib import Path

    dotenv_path = Path(__file__).parent.parent / ".env"
    load_dotenv(dotenv_path)
    DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
    DISCORD_BOT_CHANNEL_ID = os.getenv("DISCORD_BOT_CHANNEL_ID")

    send_message("Test")

from telethon import TelegramClient
from telethon.sessions import StringSession  # Import StringSession
import asyncio
import os

# Set your message and group IDs
MESSAGE = "اللّٰهُمَّ صَلِّ وَسَلِّمْ عَلٰى سَيِّدِنَا مُحَمَّد\nAllahumma salli wasallim 'ala Sayyidina Muhammad"
GROUP_IDS = [-1002288720559, -1002200241778]

async def send_message():
    api_id = int(os.getenv('API_ID'))
    api_hash = os.getenv('API_HASH')
    session_string = os.getenv('SESSION_STRING')

    # Authenticate using the session string
    async with TelegramClient(StringSession(session_string), api_id, api_hash) as client:
        for group_id in GROUP_IDS:
            await client.send_message(group_id, MESSAGE)
        print("Message sent to all groups successfully.")

if __name__ == "__main__":
    asyncio.run(send_message())

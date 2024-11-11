from telethon import TelegramClient
import asyncio
import os

# Set your message and group IDs
MESSAGE = "اللّٰهُمَّ صَلِّ وَسَلِّمْ عَلٰى سَيِّدِنَا مُحَمَّد\nAllahumma salli wasallim 'ala Sayyidina Muhammad"
GROUP_IDS = [-1002288720559, -1002200241778]

# Define a path for the session file
SESSION_FILE = "./telegram_session"

async def send_message():
    api_id = int(os.getenv('API_ID'))
    api_hash = os.getenv('API_HASH')

    async with TelegramClient(SESSION_FILE, api_id, api_hash) as client:
        for group_id in GROUP_IDS:
            await client.send_message(group_id, MESSAGE)
        print("Message sent to all groups successfully.")

if __name__ == "__main__":
    asyncio.run(send_message())

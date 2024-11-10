from telethon import TelegramClient, errors
import asyncio
import os
import time
import pytz
from datetime import timedelta

# Dapatkan API_ID, API_HASH dan nama fail sesi dari environment variables
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
session_name = os.getenv("SESSION_NAME", "my_session")  # Nama fail sesi yang digunakan

# ID kumpulan dan mesej yang ingin dihantar
group_ids = [-1002288720559, -1002200241778]  # ID kumpulan "Testing for MP CHAT" dan satu lagi kumpulan
message = """اللّٰهُمَّ صَلِّ وَسَلِّمْ عَلٰى سَيِّدِنَا مُحَمَّد
Allahumma salli wasallim 'ala Sayyidina Muhammad"""

# Buat klien Telegram
client = TelegramClient(session_name, api_id, api_hash)

# Fungsi untuk menghantar mesej
async def send_message_repeatedly():
    await client.start()  # Log masuk jika belum log masuk
    
    # Calculate time until next 5:05 PM (Malaysia Time)
    def calculate_time_to_post():
        mytz = pytz.timezone("Asia/Kuala_Lumpur")
        current_time = time.localtime()
        current_time = time.mktime(current_time)
        current_time = pytz.utc.localize(time.gmtime(current_time)).astimezone(mytz)  # Convert to MYT

        # Target time (5:05 PM Malaysia Time)
        target_time = current_time.replace(hour=17, minute=5, second=0, microsecond=0)
        
        if current_time > target_time:
            # If target time has passed for today, set for tomorrow
            target_time = target_time + timedelta(days=1)

        delay = (target_time - current_time).total_seconds()
        return delay

    try:
        # Wait until the scheduled time (5:05 PM)
        delay = calculate_time_to_post()
        print(f"Waiting for {delay} seconds until 5:05 PM...")
        await asyncio.sleep(delay)

        # After waiting, send messages
        for group_id in group_ids:
            await client.send_message(group_id, message)
            print(f"Mesej dihantar ke kumpulan {group_id}!")

    except errors.ChatAdminRequiredError:
        print("Akses ke kumpulan ini tidak dibenarkan.")
        return
    except ValueError:
        print("ID kumpulan tidak sah atau anda tidak mempunyai akses.")
        return

# Jalankan fungsi untuk menghantar mesej
with client:
    client.loop.run_until_complete(send_message_repeatedly())

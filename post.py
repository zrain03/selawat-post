from telethon import TelegramClient, errors
import asyncio
import os
import time
import pytz

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
    
    # Kirakan masa sehingga 5:30 PM (Waktu Malaysia)
    def calculate_time_to_post():
        current_time = time.localtime()
        # Set target time to 5:30 PM MYT (Malaysia Time)
        target_hour = 17  # 5:00 PM
        target_minute = 30  # 30 minutes
        target_time = time.mktime((current_time.tm_year, current_time.tm_mon, current_time.tm_mday,
                                   target_hour, target_minute, 0, current_time.tm_wday, current_time.tm_yday,
                                   current_time.tm_isdst))
        current_epoch = time.mktime(current_time)
        delay = target_time - current_epoch

        if delay < 0:
            # If target time has already passed for today, schedule for tomorrow
            delay += 86400  # Add 24 hours worth of seconds
        return delay

    try:
        # Tunggu sehingga masa yang dijadualkan (5:30 PM)
        delay = calculate_time_to_post()
        print(f"Waiting for {delay} seconds until 5:30 PM...")
        await asyncio.sleep(delay)

        # Setelah menunggu, hantar mesej
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

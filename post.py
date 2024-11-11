from telethon import TelegramClient, errors
import asyncio
import os
import time
import pytz

# Get API_ID, API_HASH, and session file name from environment variables
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
session_name = os.getenv("SESSION_NAME", "my_session")  # Session file name used

# Group IDs and message to be sent
group_ids = [-1002288720559, -1002200241778]  # Replace with your actual group IDs
message = """اللّٰهُمَّ صَلِّ وَسَلِّمْ عَلٰى سَيِّدِنَا مُحَمَّد
Allahumma salli wasallim 'ala Sayyidina Muhammad"""

# Create the Telegram client
client = TelegramClient(session_name, api_id, api_hash)

# Function to send the message at the scheduled time
async def send_message_repeatedly():
    await client.start()  # Log in if not already logged in
    
    # Calculate time to the next 5:00 PM (MYT)
    def calculate_time_to_post():
        # Set timezone to MYT (Malaysia Time, UTC+8)
        timezone = pytz.timezone('Asia/Kuala_Lumpur')
        current_time = time.localtime()
        
        # Current time in MYT
        current_time_obj = time.struct_time(current_time)
        now = pytz.utc.localize(time.mktime(current_time_obj))  # UTC time
        
        # Target time for 5:00 PM MYT (Malaysia Time)
        target_hour = 17  # 5:00 PM
        target_time = now.replace(hour=target_hour, minute=0, second=0, microsecond=0)
        
        # If target time already passed today, schedule for tomorrow
        if now > target_time:
            target_time += timedelta(days=1)
        
        delay = (target_time - now).total_seconds()
        return delay

    try:
        # Wait until the scheduled time (5:00 PM)
        delay = calculate_time_to_post()
        print(f"Waiting for {delay} seconds until 5:00 PM MYT...")
        await asyncio.sleep(delay)

        # Send the message to all the groups
        for group_id in group_ids:
            await client.send_message(group_id, message)
            print(f"Message sent to group {group_id}!")

    except errors.ChatAdminRequiredError:
        print("Access to this group is not allowed.")
        return
    except ValueError:
        print("Invalid group ID or you don't have access.")
        return

# Run the function to send the message
with client:
    client.loop.run_until_complete(send_message_repeatedly())

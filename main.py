import asyncio
import os
import re
from telethon.sync import TelegramClient
from telethon.tl.types import InputPeerChannel
from telethon.tl.functions.messages import GetMessagesRequest
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.errors import FloodWaitError

# ==== CONFIGURATION ====
api_id = 10039364           # Replace with your own API ID
api_hash = '63f5e9ca5613f8830cb8c3441ea04c01'    # Replace with your own API hash
phone_number = '+919327385032'  # Your phone number with country code
upload_target = 'vipulrestricted'  # Your own channel or chat to upload to

client = TelegramClient("session", api_id, api_hash)

async def main():
    await client.start(phone_number)

    chat_input = input("Enter Telegram message link or channel username (e.g., https://t.me/c/... or @channel): ").strip()
    start_id = int(input("Enter START message ID (e.g., 15551): "))
    limit = int(input("How many messages to process?: "))

    # Extract chat ID from /c/ link
    if '/c/' in chat_input:
        match = re.search(r'/c/(\d+)', chat_input)
        if not match:
            print("❌ Invalid /c/ link format.")
            return
        chat_id = int(match.group(1))
        try:
            dialogs = await client.get_dialogs()
            target_chat = next((d for d in dialogs if d.entity.id == chat_id), None)
            if not target_chat:
                print("❌ Chat not found in your dialog list. Open it in Telegram first.")
                return
            entity = target_chat.entity
        except Exception as e:
            print(f"❌ Error resolving chat: {e}")
            return
    else:
        entity = await client.get_entity(chat_input)

    os.makedirs("downloads", exist_ok=True)

    for i in range(limit):
        msg_id = start_id + i
        print(f"[{i+1}/{limit}] ({int((i+1)/limit*100)}%) Processing message {msg_id}...")

        try:
            msg = await client.get_messages(entity, ids=msg_id)

            if not msg:
                print(f"⚠️ Message {msg_id} not found.")
                continue

            if msg.media:
                file_path = await client.download_media(msg, file=f"downloads/{msg_id}")
                print(f"✅ Downloaded: {file_path}")

                print(f"📤 Uploading {os.path.basename(file_path)} to @{upload_target} ...")
                await client.send_file(upload_target, file_path, caption=msg.message or "")
                print(f"✅ Uploaded successfully.")
            else:
                print(f"ℹ️ Message {msg_id} has no downloadable media.")

        except FloodWaitError as e:
            print(f"🚫 Flood wait error. Sleeping for {e.seconds} seconds...")
            await asyncio.sleep(e.seconds)
        except Exception as e:
            print(f"❌ Error in message {msg_id}: {e}")

    print("🎉 Done processing all messages.")

# ==== RUN ====
if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())

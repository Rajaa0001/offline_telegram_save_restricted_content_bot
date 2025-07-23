# 📥 Telegram Restricted Content Saver & Uploader Bot

This Python script allows you to **download restricted content** from private Telegram channels and **automatically upload it** to another Telegram channel using your user credentials (not a bot).

## ✅ Features

- 🔒 Bypass restricted content access using your Telegram user session
- 📂 Download all media types: images, videos, files (ZIP, PDF, XLSX, etc.)
- 📤 Auto-upload each downloaded message to a target channel (e.g., `@yourchannel`)
- 📈 Shows per-message progress and tracks what's done
- 📋 Works with both channel usernames and full t.me/c/... message links
- 💾 Supports `.session` file reuse (no repeated logins)

## ⚙️ How to Use

1. Clone or download this repo
2. Install dependencies:
   ```bash
   pip install telethon
3. Replace your credentials in main.py:
api_id, api_hash from my.telegram.org
Your phone number

4.Run the script:
python main.py
Provide:
Source message or channel link
Start message ID
Number of messages to process

if you need any help contact telegram @the_vipul_solanki

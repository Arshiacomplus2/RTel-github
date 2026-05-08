import os
import sys
from telethon.sync import TelegramClient
from telethon.sessions import StringSession
from utils import load_json, save_json, manage_archives, DATA_DIR


API_ID_ENV = os.environ.get('TG_API_ID', '').strip()
API_HASH_ENV = os.environ.get('TG_API_HASH', '').strip()
SESSION = os.environ.get('TG_SESSION', '').strip()
BOT_TOKEN = os.environ.get('TG_BOT_TOKEN', '').strip()
CHANNELS = os.environ.get('TARGET_CHANNELS', '').split(',')


if not API_ID_ENV or not API_HASH_ENV:
    API_ID = 6
    API_HASH = "eb06d4abfb49dc3eeb1aeb98ae0f581e"
else:
    API_ID = int(API_ID_ENV)
    API_HASH = API_HASH_ENV

if not SESSION and not BOT_TOKEN:
    print("❌ Error: You must provide either TG_SESSION (Userbot) or TG_BOT_TOKEN (Bot)!")
    sys.exit(1)


session_storage = StringSession(SESSION) if SESSION else StringSession('')
client = TelegramClient(session_storage, API_ID, API_HASH)

def fetch_messages():
    state_file = os.path.join(DATA_DIR, 'sync_state.json')
    latest_file = os.path.join(DATA_DIR, 'latest.json')

    state = load_json(state_file, {})
    messages = load_json(latest_file,[])


    if BOT_TOKEN:
        print("🤖 Starting in BOT mode...")
        client.start(bot_token=BOT_TOKEN)
    else:
        print("👤 Starting in USERBOT mode...")
        client.start()

    with client:
        for channel in CHANNELS:
            channel = channel.strip()
            if not channel:
                continue

            last_id = state.get(channel, 0)
            print(f"📡 Checking channel {channel} from message ID {last_id} onwards...")

            new_msgs =[]
            try:
                for msg in client.iter_messages(channel, min_id=last_id, limit=50):
                    if msg.text:
                        new_msgs.append({
                            "id": msg.id,
                            "channel": channel,
                            "date": msg.date.isoformat(),
                            "text": msg.text
                        })
            except Exception as e:
                print(f"⚠️ Could not fetch {channel}. Error: {str(e)}")
                continue

            if new_msgs:
                new_msgs.sort(key=lambda x: x['id'], reverse=True)
                state[channel] = new_msgs[0]['id']
                messages = new_msgs + messages
                print(f"✅ Successfully fetched {len(new_msgs)} new messages from {channel}.")
            else:
                print(f"ℹ️ No new messages found in {channel}.")

    save_json(state_file, state)
    save_json(latest_file, messages)
    manage_archives()
    print("🚀 Sync process finished successfully.")

if __name__ == '__main__':
    fetch_messages()
import os
import sys
from telethon.sync import TelegramClient
from telethon.sessions import StringSession
from utils import load_json, save_json, manage_archives, DATA_DIR


API_ID = int(os.environ.get('TG_API_ID', 0))
API_HASH = os.environ.get('TG_API_HASH', '')
SESSION = os.environ.get('TG_SESSION', '')

CHANNELS = os.environ.get('TARGET_CHANNELS', '').split(',')

if not API_ID or not API_HASH or not SESSION:
    print("❌ Error: Telegram credentials (Secrets) are not configured!")
    sys.exit(1)

client = TelegramClient(StringSession(SESSION), API_ID, API_HASH)

def fetch_messages():
    state_file = os.path.join(DATA_DIR, 'sync_state.json')
    latest_file = os.path.join(DATA_DIR, 'latest.json')

    state = load_json(state_file, {})
    messages = load_json(latest_file,[])

    with client:
        for channel in CHANNELS:
            channel = channel.strip()
            if not channel:
                continue

            last_id = state.get(channel, 0)
            print(f"📡 Checking channel {channel} from message ID {last_id} onwards...")

            new_msgs =[]

            for msg in client.iter_messages(channel, min_id=last_id, limit=50):
                if msg.text:
                    new_msgs.append({
                        "id": msg.id,
                        "channel": channel,
                        "date": msg.date.isoformat(),
                        "text": msg.text
                    })

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
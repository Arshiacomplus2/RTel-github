import os
import sys
from telethon.sync import TelegramClient
from utils import load_json, save_json, manage_archives, DATA_DIR


BOT_TOKEN = os.environ.get('TG_BOT_TOKEN', '').strip()
CHANNELS = os.environ.get('TARGET_CHANNELS', '').split(',')

if not BOT_TOKEN:
    print("❌ Error: TG_BOT_TOKEN is missing! Please set it in GitHub Secrets.")
    sys.exit(1)


API_ID = 6
API_HASH = "eb06d4abfb49dc3eeb1aeb98ae0f581e"

client = TelegramClient('bot_session', API_ID, API_HASH)

def fetch_messages():
    state_file = os.path.join(DATA_DIR, 'sync_state.json')
    latest_file = os.path.join(DATA_DIR, 'latest.json')

    state = load_json(state_file, {})
    messages = load_json(latest_file,[])

    print("🤖 Starting in BOT mode...")
    client.start(bot_token=BOT_TOKEN)

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
                print(f"⚠️ Could not fetch {channel}. Ensure the bot is an admin in the channel. Error: {str(e)}")
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
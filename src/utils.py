import json
import os

DATA_DIR = 'data'
ARCHIVE_DIR = os.path.join(DATA_DIR, 'archive')


os.makedirs(ARCHIVE_DIR, exist_ok=True)

def load_json(filepath, default_value):
    if not os.path.exists(filepath):
        return default_value
    with open(filepath, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return default_value

def save_json(filepath, data):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def manage_archives():
    latest_file = os.path.join(DATA_DIR, 'latest.json')
    index_file = os.path.join(DATA_DIR, 'index.json')

    messages = load_json(latest_file,[])


    if len(messages) > 100:

        kept_messages = messages[:100]

        to_archive = messages[100:]

        archive_index = load_json(index_file, {"archives": []})
        new_archive_name = f"archive_{len(archive_index['archives']) + 1}.json"


        save_json(os.path.join(ARCHIVE_DIR, new_archive_name), to_archive)


        archive_index['archives'].append(new_archive_name)
        save_json(index_file, archive_index)


        save_json(latest_file, kept_messages)
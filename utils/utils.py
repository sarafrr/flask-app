import json

def load_data(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        # raw = f.read()
        # raw = raw.replace('\\', '\\\\')
        # # Remove or escape invalid control characters
        # cleaned = re.sub(r'[\x00-\x1F]+', ' ', raw)
        # data = json.loads(cleaned)
        data = json.load(f)
    return data

def save_data(file_path, data):
    with open(file_path, "w+", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
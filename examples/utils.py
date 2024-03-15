import json

def write_json(data, path):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii = False, indent = 2)

def read_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)
    

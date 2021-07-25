import json

with open('./data/status.json', 'r') as status_json:
    status = json.load(status_json)

def update_status(data):
    with open('./data/status.json', 'w') as status_json:
        status_json.write(json.dumps(data, indent=4))
import json

def save_to_json(slides_summary, json_file):
    with open(json_file, 'w') as f:
        json.dump(slides_summary, f, indent=4)
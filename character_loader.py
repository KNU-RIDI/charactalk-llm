import json

def load_all_characters():
    with open("prompts.json", "r", encoding="utf-8") as f:
        prompts_data = json.load(f)

    return prompts_data
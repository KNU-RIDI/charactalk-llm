import json

def load_character(character_name):
    with open("prompts.json", "r", encoding="utf-8") as f:
        prompts_data = json.load(f)

    return prompts_data.get(character_name, None)
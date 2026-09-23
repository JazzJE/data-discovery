import json
from config import Config

with open(Config.FolderPaths.INORGANIC_DATASET, "r") as f:
    data = json.load(f)


def get_keys(value):
    keys = set()

    if isinstance(value, dict):
        keys.update(value.keys())
        for nested_value in value.values():
            keys.update(get_keys(nested_value))
    elif isinstance(value, list):
        for nested_value in value:
            keys.update(get_keys(nested_value))

    return keys


if isinstance(data, dict):
    all_keys = set()
    for value in data.values():
        all_keys.update(get_keys(value))
else:
    all_keys = get_keys(data)

print(all_keys) 
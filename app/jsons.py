from json import load, dump, decoder

def load_data(file_name: str) -> dict:
    try:
        with open(file_name, 'r') as file:
            return load(file)
    except (FileNotFoundError, decoder.JSONDecodeError):
        return {}

def dump_data(file_name: str, data: dict) -> None:
    with open(file_name, 'w') as file:
        dump(data, file, indent=2)
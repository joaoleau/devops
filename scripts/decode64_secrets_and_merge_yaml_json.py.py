import yaml
import json
import base64

description = """
This script decodes base64-encoded values from a YAML file (sealed_secrets.yaml)
and integrates them into a JSON file (parameter.json). It parses the YAML data, 
decodes each base64-encoded value, and merges the decoded values with corresponding 
entries in the JSON file. The updated JSON data is then saved to a new file (new_parameter.json)
in a formatted manner.
"""


def load_json_with_decoded_values(json_file, decode_data):
    new_json_file = []

    parameter_names =  [parameter.get("Name").strip() for parameter in json_file]
    parameter_suffixes = [parameter.get("Name").strip().split("/")[-1] for parameter in json_file]
    
    for key_data, value_data in decode_data.items():
        if key_data in parameter_suffixes:
            new_json_file.append({"Name": parameter_names[parameter_suffixes.index(key_data)], "Value": value_data})

    return new_json_file


def yaml_decode_data(yaml_data_file):
    decode_data = {}
    for key, value in yaml_data_file.items():
        decoded_bytes = base64.b64decode(value)
        decoded_string = decoded_bytes.decode('utf-8')
        decode_data[key] = decoded_string

    return decode_data


if __name__ == "__main__":
    with open("secrets/sealed_secrets.yaml", "r", encoding="utf-8") as file:
        yaml_file = yaml.safe_load(file)

    with open("secrets/parameter.json", "r", encoding="utf-8") as raw_parameter:
        json_file = json.load(raw_parameter)
    
    decode_data = yaml_decode_data(yaml_file.get("data"))
    new_json_file = load_json_with_decoded_values(json_file, decode_data)
    
    with open("secrets/new_parameter.json", "w", encoding="utf-8") as json_file:
        json.dump(new_json_file, json_file, ensure_ascii=False, indent=4)
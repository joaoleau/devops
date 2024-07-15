import os

description = """
This script searches for YAML files in the current directory and its subdirectories,
then checks these files for specific key-value pairs. Specifically, it looks for files where:

    * The key kind has a value that is Deployment or Application.
    * The key secretName is present.
"""

NOT_DIRS = []

def is_valid_key_value(key, value):
    if key == "kind" and value not in ["Deployment", "Application"]:
        return
    if key == "secretName":
        return key, value
    return

def parse_yaml_file(file_path):
    with open(file_path, 'r') as yaml_file:
        for line in yaml_file:
            key_value_pair = line.strip().split(":")
            if len(key_value_pair) > 1:
                key = key_value_pair[0].strip()
                value = key_value_pair[1].strip()
                if is_valid_key_value(key, value):
                    return file_path
    return

def find_yaml_files(directory):
    yaml_files = []
    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if d not in NOT_DIRS]
        
        for file in files:
            if file.endswith(".yaml") or file.endswith(".yml"):
                file_path = os.path.join(root, file)
                if parse_yaml_file(file_path):
                    yaml_files.append(file_path)
    return yaml_files

if __name__ == "__main__":
    current_directory = os.getcwd()
    found_files = find_yaml_files(current_directory)

    if found_files:
        print("Files found:")
        for file in found_files:
            print(file)
    else:
        print("No files found with the specified keys.")
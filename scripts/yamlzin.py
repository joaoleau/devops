import yaml
import os


class ScriptClass:
    config_file = None
    yaml_file = None
    files_found = []

    def __init__(self, path_config):
        with open(path_config, "r") as config:
            self.config_file = yaml.safe_load(config)

    def validate(self):
        return self.yaml_file is not None

    def find_yaml_files(self, path):
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.endswith(".yaml") or file.endswith(".yml"):
                    file_path = os.path.join(root, file)
                    self.open_yaml_file(file_path)

                    if self.validate():
                        print(self.yaml_file, file_path)
                        self.files_found.append(file_path)   

    def open_yaml_file(self, file_path):
        with open(file_path, "r") as file:
            self.yaml_file = yaml.safe_load(file)
            self.open_config_key(self.config_file)
    
    def open_yaml_key(self, key_name):
        if isinstance(self.yaml_file, list):
            self.yaml_file = self.yaml_file[0]
        if self.yaml_file:
            self.yaml_file = self.yaml_file.get(key_name)
    
    def open_config_key(self, key):
        key_name = list(key.keys())[0]
        p_key = key.get(key_name, None)

        if p_key:
            self.open_yaml_key(key_name)
            key = p_key
            return self.open_config_key(key)
        
        return key
             

if __name__ == "__main__":
    config_path = "./search.yaml"
    current_directory = os.getcwd()
    sc = ScriptClass(config_path)
    sc.find_yaml_files(current_directory)
    
    for file in sc.files_found:
        print(file)




    # current_directory = os.getcwd()
    # found_files = find_yaml_files(current_directory)
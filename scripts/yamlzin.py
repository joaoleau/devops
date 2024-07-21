import yaml
import os


class ScriptClass:
    path_initial = None
    config_file = None
    
    yaml_file_tmp = None
    file_path_tmp = None
    arquivo_e_verdadeiro_tmp = None
    acabou_validacao_tmp = None
    
    founds = {}
    validados = {}


    def __init__(self, path_config, path_initial):
        self.path_initial = path_initial
        with open(path_config, "r") as config:
            self.config_file = yaml.safe_load(config)
    

    def executar(self):
        self.buscar_arquivos_yaml()
        self.buscador_nos_arquivos_yamls_encontrados()



    def buscar_arquivos_yaml(self):
        for root, dirs, files in os.walk(self.path_initial):
            for file in files:           
                if self.arquivo_eh_yaml(file):
                    self.file_path_tmp = os.path.join(root, file)                    
                    self.founds[self.file_path_tmp] = file


    def arquivo_eh_yaml(self, file):
        if file == "config.yaml":
            return
        
        return file.endswith(".yaml") or file.endswith(".yml")
    

    def buscador_nos_arquivos_yamls_encontrados(self):
        for file_path in self.founds:
            self.file_path_tmp = file_path
            self.arquivo_e_verdadeiro_tmp = True
            self.abrir_arquivo_yaml_encontrado()
            arquivo_validado = self.validar_arquivo_e_retornar_conteudo_encontrado()
            if arquivo_validado:
                self.adicionar_arquivo_na_lista_de_validados()


    def abrir_arquivo_yaml_encontrado(self):
        with open(self.file_path_tmp, "r") as file:
            self.yaml_file_tmp = yaml.safe_load(file)


    def validar_arquivo_e_retornar_conteudo_encontrado(self):        
        self.comparar_file_com_key_value(self.config_file)
        if self.arquivo_e_verdadeiro_tmp and self.acabou_validacao_tmp:
            return True

        if not self.arquivo_e_verdadeiro_tmp and self.acabou_validacao_tmp:
            return
        

    def comparar_file_com_key_value(self, keys_and_values=None):
        if not self.yaml_file_tmp:
            return
        
        items = keys_and_values.items()
        for key, value in items:
            if key and isinstance(value, dict):
                self.recebe_uma_key_e_entra_no_arquivo(key)
                return self.comparar_file_com_key_value(value)
            
            self.recebe_uma_key_e_entra_no_arquivo(key, value)
        
        self.acabou_validacao_tmp = True
        return


    def recebe_uma_key_e_entra_no_arquivo(self, key, value=None):
        
        if self.yaml_file_tmp and isinstance(self.yaml_file_tmp, dict):
            
            if key and not value:
                self.yaml_file_tmp = self.yaml_file_tmp.get(key)

            if value:
                file_valid = self.validar_yaml_tmp_com_resultado_esperado(file=self.yaml_file_tmp, key=key, value=value)
                if not file_valid:
                    self.arquivo_e_verdadeiro_tmp = False
                self.yaml_file_tmp = file_valid

            if self.yaml_file_tmp and not isinstance(self.yaml_file_tmp, dict):
                self.yaml_file_tmp = yaml.safe_load(self.yaml_file_tmp)


    def validar_yaml_tmp_com_resultado_esperado(self, **kwargs):
        if not kwargs and self.yaml_file_tmp:
            return self.yaml_file_tmp

        file = kwargs.get("file", None)
        if file:
            value = kwargs.get("value")
            key = kwargs.get("key")
            file_key_value = file.get(key)
            if file_key_value == value:
                return file 
        
        return


    def adicionar_arquivo_na_lista_de_validados(self):
        self.validados[self.file_path_tmp] = self.yaml_file_tmp     
             

if __name__ == "__main__":
    
    config_path = "config.yaml"
    # current_directory = os.getcwd()
    current_directory = "."
    
    
    sc = ScriptClass(config_path, current_directory)
    sc.executar()
    
    for key, value in sc.validados.items():
        print(key, value)
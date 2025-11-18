import json

def load_metadata(filepath):
    try:
        with open(filepath, 'r', encoding = 'utf-8') as file:
            data = json.load(file)  
            return data  
    except:
        return {}
        raise FileNotFoundError
        
def save_metadata(filepath, data):
    with open(filepath, 'w', encoding = 'utf-8') as file:
        json.dump(data, file)

def load_table_data(table_name):
    try:
        filepath = "./data/" + table_name + '.json'
        with open(filepath, 'r', encoding = 'utf-8') as file:
            data = json.load(file)  
            return data  
    except:
        return []

def save_table_data(table_name, data):
    filepath = "./data/" + table_name + '.json'
    with open(filepath, 'w', encoding = 'utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=2)
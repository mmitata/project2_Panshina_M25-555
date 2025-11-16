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
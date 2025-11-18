from src.primitive_db.utils import load_table_data, save_table_data

def create_table(metadata, table_name, columns):
    if table_name in metadata:
        print(f'Ошибка: Таблица "{table_name}" уже существует.') 
    else:
        for col in columns:
            name, c_type = col.split(':')
            if c_type not in ['int', 'str', 'bool']:
                raise TypeError
        columns.insert(0, 'ID:int')
        metadata[table_name] = columns
        print(f'Таблица "{table_name}" успешно создана со столбцами: {', '.join(columns)}') 

def drop_table(metadata, table_name):
    if table_name not in metadata: 
        raise Exception(f'Ошибка: Таблица "{table_name}" не существует')
    else:
        metadata.pop(table_name)
        print(f'Таблица "{table_name}" успешна удалена.')

def insert(metadata, table_name, values):
    if table_name not in metadata: 
        raise Exception(f'Ошибка: Таблица "{table_name}" не существует')
    
    table_schema = metadata[table_name][1:]
    
    if len(values) != len(table_schema):
        raise Exception(f'Количество столбцов не соответствует таблице {table_name}.')
    
    converted_values = dict()
    data = load_table_data(table_name)
    ID = len(data) + 1
    converted_values["ID"] = ID
    for i, (value, column_def) in enumerate(zip(values, table_schema)):
        column_name, expected_type = column_def.split(':')
        expected_type = expected_type.strip()
        converted_value = ''
        if expected_type == 'int':
            converted_value = int(value)
        elif expected_type == 'str':
            converted_value = str(value)
        elif expected_type == 'bool':
            if isinstance(value, str):
                if value.lower() == 'true':
                    converted_value = True
                elif value.lower() == 'false':
                    converted_value = False
                else:
                    raise ValueError(f"Неверное булево значение: {value}")
            else:
                converted_value = bool(value)
        else:
            raise Exception(f'Неизвестный тип данных: {expected_type}')
        
        converted_values[column_name] = converted_value
    data.append(converted_values)
    
    return data
    
def select(table_data, where_clause=None):
    if where_clause is None:
        return table_data
    filtered_data = []
    [(column, value)] = list(where_clause.items())
    for record in table_data:
        if record[column] == value:
            filtered_data.append(record)

    return filtered_data

def update(table_data, set_clause, where_clause):
    [(set_column, set_value)] = list(set_clause.items())
    [(where_column, where_value)] = list(where_clause.items())
    ids = []
    for record in table_data:
        if record[where_column] == where_value:
            record[set_column] = set_value
            ids.append(record['ID'])
    return table_data, ids

def delete(table_data, where_clause):
    [(where_column, where_value)] = list(where_clause.items())
    ids = [item["ID"] for item in table_data if item[where_column] == where_value]
    updated_data =[item for item in table_data if item[where_column] != where_value]
    return updated_data, ids

# insert into users values ("Sergei", 28, true)
# update users set age = 29 where name = "Sergei"
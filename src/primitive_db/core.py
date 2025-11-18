import json

from src.decorators import confirm_action, handle_db_errors, log_time
from src.primitive_db.utils import load_table_data, save_table_data


def create_cacher():
    cache = {}

    def cache_result(key, value_func):
        if key in cache:
            return cache[key]
        result = value_func()
        cache[key] = result
        return result

    return cache_result

select_cache = create_cacher()

@handle_db_errors
@log_time
def create_table(metadata, table_name, columns):
    if table_name in metadata:
        raise Exception(f'Таблица "{table_name}" уже существует.') 
    else:
        for col in columns:
            name, c_type = col.split(':')
            if c_type not in ['int', 'str', 'bool']:
                raise TypeError(f'Неверно выбран тип для данных: {c_type}')
        columns.insert(0, 'ID:int')
        metadata[table_name] = columns
        print(
            f'Таблица "{table_name}" успешно создана со столбцами: '
            f"{', '.join(columns)}")

@handle_db_errors
@confirm_action('удаление таблицы')
def drop_table(metadata, table_name):
    if table_name not in metadata: 
        raise Exception(f'Таблица "{table_name}" не существует')
    else:
        metadata.pop(table_name)
        print(f'Таблица "{table_name}" успешна удалена.')

@handle_db_errors
@log_time
def insert(metadata, table_name, values):
    if table_name not in metadata: 
        raise Exception(f'Таблица "{table_name}" не существует')
    
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
    save_table_data(table_name, data)

@handle_db_errors
@log_time
def cached_select(table_name, where_clause=None):
    table_data = load_table_data(table_name)
    cache_key = json.dumps({
        "table": table_name,
        "where": where_clause
    }, sort_keys=True)

    def compute():
        if where_clause is None:
            return table_data

        filtered = []
        [(column, value)] = list(where_clause.items())
        for record in table_data:
            if record.get(column) == value:
                filtered.append(record)
        return filtered

    return select_cache(cache_key, compute)

@handle_db_errors
@log_time
def update(table_name, set_clause, where_clause):
    table_data = load_table_data(table_name)
    [(set_column, set_value)] = list(set_clause.items())
    [(where_column, where_value)] = list(where_clause.items())
    ids = []
    for record in table_data:
        if record[where_column] == where_value:
            record[set_column] = set_value
            ids.append(record['ID'])
    save_table_data(table_name, table_data)
    return ids

@handle_db_errors
@confirm_action('удаление записи')
@log_time
def delete(table_name, where_clause):
    table_data = load_table_data(table_name)
    [(where_column, where_value)] = list(where_clause.items())
    ids = [item["ID"] for item in table_data if item[where_column] == where_value]
    updated_data =[item for item in table_data if item[where_column] != where_value]
    save_table_data(table_name, updated_data)
    return ids

@handle_db_errors
def info(args, metadata):
    table_name = args[1]
    data_len = len(load_table_data(table_name))
    columns = metadata[table_name]
    print(
        f"Таблица: {table_name}\n"
        f"Столбцы: {', '.join(columns)}\n"
        f"Количество записей: {data_len}")
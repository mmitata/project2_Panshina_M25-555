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
        print(f'Ошибка: Таблица "{table_name}" не существует')
    else:
        metadata.pop(table_name)
        print(f'Таблица "{table_name}" успешна удалена.')
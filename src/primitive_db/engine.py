import shlex

import prompt
from prettytable import PrettyTable

from src.primitive_db.core import (
    cached_select,
    create_table,
    delete,
    drop_table,
    info,
    insert,
    select_cache,
    update,
)
from src.primitive_db.parser import parse_command
from src.primitive_db.utils import load_metadata, save_metadata


def print_help():
    """Prints the help message for the current mode."""
   
    print("\n***Процесс работы с таблицей***")
    print("Функции:")
    print("<command> create_table <имя_таблицы> <столбец1:тип> .. - создать таблицу")
    print("<command> list_tables - показать список всех таблиц")
    print("<command> drop_table <имя_таблицы> - удалить таблицу")
    print(
        "<command> insert into <имя_таблицы> "
        "values (<значение1>, <значение2>, ...) - создать запись.")
    print(
        "<command> select from <имя_таблицы> "
        "where <столбец> = <значение> - прочитать записи по условию.")
    print("<command> select from <имя_таблицы> - прочитать все записи.")
    print(
        "<command> update <имя_таблицы> set <столбец1> = <новое_значение1> "
        "where <столбец_условия> = <значение_условия> - обновить запись.")
    print(
        "<command> delete from <имя_таблицы> "
        "where <столбец> = <значение> - удалить запись.")
    print("<command> info <имя_таблицы> - вывести информацию о таблице.")
    
    print("\nОбщие команды:")
    print("<command> exit - выход из программы")
    print("<command> help - справочная информация\n") 
        
    
def run():
    while True:
        user_input = prompt.string('>>> Введите команду: ')
        data_path = './db_meta.json'
        metadata = load_metadata(data_path)
        args = shlex.split(user_input)
        match args[0]:
            case 'help':
                print_help()
            case 'exit':
                break
            case 'create_table':
                create_table(metadata, args[1], args[2:])
                save_metadata(data_path, metadata)
            case 'list_tables':
                print('\n'.join(list(metadata.keys())))
            case 'drop_table':
                try:
                    drop_table(metadata, args[1])
                    save_metadata(data_path, metadata)
                except Exception:
                    print(Exception)
            case 'insert':
                values = ' '.join(args[4:]).strip('()').split(", ")
                table_name = args[2]
                insert(metadata, table_name, values)
                invalidate_cache_for(table_name)
            case 'select':
                where_clause = None
                if len(args) > 3:
                    where_clause = ' '.join(args[4:])
                table_name = args[2]
                filtered_data = cached_select(table_name, parse_command(where_clause))
                table = PrettyTable()
                table.field_names = list(filtered_data[0].keys())
                for row in filtered_data:
                    table.add_row([row.get(header, '') for header in table.field_names])
                print(table)
            case 'update':
                set_clause = ' '.join(args[3:6])
                where_clause = ' '.join(args[7:])
                table_name = args[1]
                ids = update(
                    table_name, 
                    parse_command(set_clause), 
                    parse_command(where_clause))
                invalidate_cache_for(table_name)
                for ID in ids:
                    print(f'Запись с ID={ID} в таблице {table_name} успешно обновлена.')
            case 'delete':
                where_clause = ' '.join(args[4:])
                table_name = args[2]
                ids = delete(table_name, parse_command(where_clause))
                invalidate_cache_for(table_name)
                for ID in ids:
                    print(f'Запись с ID={ID} успешно удалена из таблицы {table_name}.')
            case 'info':
                info(args, metadata)
            case _:
                print(f'Функции {args[0]} нет. Попробуйте снова.')



def invalidate_cache_for(table_name):
    old_cache = select_cache.__closure__[0].cell_contents
    keys_to_remove = [k for k in old_cache if f'"table": "{table_name}"' in k]
    for k in keys_to_remove:
        del old_cache[k]
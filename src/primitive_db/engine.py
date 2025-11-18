import prompt
import shlex
from src.primitive_db.core import create_table, drop_table, insert, select, update, delete
from src.primitive_db.utils import save_metadata, load_metadata, load_table_data, save_table_data
from src.primitive_db.parser import parse_command
from prettytable import PrettyTable
def print_help():
    """Prints the help message for the current mode."""
   
    print("\n***Процесс работы с таблицей***")
    print("Функции:")
    print("<command> create_table <имя_таблицы> <столбец1:тип> .. - создать таблицу")
    print("<command> list_tables - показать список всех таблиц")
    print("<command> drop_table <имя_таблицы> - удалить таблицу")
    
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
                try:
                    values = ' '.join(args[4:]).strip('()').split(", ")
                    table_name = args[2]
                    save_table_data(table_name, insert(metadata, table_name, values))
                except Exception as e:
                    raise e
            case 'select':
                where_clause = None
                if len(args) > 3:
                    where_clause = ' '.join(args[4:])
                filtered_data = select(load_table_data(args[2]), parse_command(where_clause))
                table = PrettyTable()
                table.field_names = list(filtered_data[0].keys())
                for row in filtered_data:
                    table.add_row([row.get(header, '') for header in table.field_names])
                print(table)
            case 'update':
                set_clause = ' '.join(args[3:6])
                where_clause = ' '.join(args[7:])
                table_name = args[1]
                data, ids = update(load_table_data(table_name), parse_command(set_clause), parse_command(where_clause))
                save_table_data(table_name, data)
                for ID in ids:
                    print(f'Запись с ID={ID} в таблице {table_name} успешно обновлена.')
            case 'delete':
                where_clause = ' '.join(args[4:])
                table_name = args[2]
                data, ids = delete(load_table_data(table_name), parse_command(where_clause))
                save_table_data(table_name, data)
                for ID in ids:
                    print(f'Запись с ID={ID} успешно удалена из таблицы {table_name}.')
            case 'info':
                table_name = args[1]
                data_len = len(load_table_data(table_name))
                columns = metadata[table_name]
                print(f'Таблица: {table_name}\nСтолбцы: {', '.join(columns)}\nКоличество записей: {data_len}')
            case _:
                print(f'Функции {args[0]} нет. Попробуйте снова.')



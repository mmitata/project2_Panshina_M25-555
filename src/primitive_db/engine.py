import prompt
import shlex
from src.primitive_db.core import create_table, drop_table
from src.primitive_db.utils import save_metadata, load_metadata

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
        user_input = prompt.string('Введите команду: ')
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
                drop_table(metadata, args[1])
                save_metadata(data_path, metadata)
            case _:
                print(f'Функции {args[0]} нет. Попробуйте снова.')



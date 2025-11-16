from src.primitive_db.engine import run, print_help
import prompt
import shlex
import json
from src.primitive_db.core import create_table, drop_table
from src.primitive_db.utils import save_metadata, load_metadata


def main():
    print('DB project is running!')
    print_help()
    run()

if __name__ == "__main__":
    main()
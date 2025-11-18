import time


def handle_db_errors(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except FileNotFoundError:
            print("Ошибка: Файл данных не найден. "
            "Возможно, база данных не инициализирована.")
        except KeyError as e:
            print(f"Ошибка: Таблица или столбец {e} не найден.")
        except ValueError as e:
            print(f"Ошибка валидации: {e}")
        except Exception as e:
            print(f"Произошла непредвиденная ошибка: {e}")
    return wrapper

def confirm_action(action_name):
    """
    Фабрика декораторов.
    Возвращает декоратор, который спрашивает у 
    пользователя подтверждение перед выполнением функции.
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            answer = input(
                f"Вы уверены, что хотите выполнить действие: {action_name}? (y/n): "
                ).strip().lower()
            if answer == "y":
                return func(*args, **kwargs)
            else:
                print("Действие отменено.")
        return wrapper
    return decorator


def log_time(func):
    def wrapper(*args, **kwargs):
        start = time.monotonic()
        result = func(*args, **kwargs)
        end = time.monotonic()
        duration = end - start
        print(f"Функция {func.__name__} выполнилась за {duration:.3f} секунд.")
        return result
    return wrapper

import threading
import json
import os
import math

USER_DATA_FILE = 'users.json'
CALC_HISTORY_FILE = 'calc_history.json'

def init_files():
    if not os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, 'w') as f:
            json.dump({}, f)

    if not os.path.exists(CALC_HISTORY_FILE):
        with open(CALC_HISTORY_FILE, 'w') as f:
            json.dump([], f)

def load_users():
    with open(USER_DATA_FILE, 'r') as f:
        return json.load(f)

def save_users(users):
    with open(USER_DATA_FILE, 'w') as f:
        json.dump(users, f, indent=4)

def register():
    users = load_users()
    username = input("Введите имя пользователя: ")
    if username in users:
        print("Пользователь уже существует.")
    else:
        password = input("Введите пароль: ")
        users[username] = password
        save_users(users)
        print("Регистрация успешна.")

def login():
    users = load_users()
    username = input("Введите имя пользователя: ")
    password = input("Введите пароль: ")
    if username in users and users[username] == password:
        print("Авторизация успешна.")
        return username
    else:
        print("Неверное имя пользователя или пароль.")
        return None

def calculate():
    while True:
        operation = input("\nВведите операцию ( +, -, *, /, **, sqrt или 'exit' для выхода): ")
        if operation == 'exit':
            break
        if operation in ['+', '-', '*', '/', '**', 'sqrt']:
            if operation == 'sqrt':
                num = float(input("Введите число для нахождения корня: "))
                result = math.sqrt(num)
            else:
                num1 = float(input("Введите первое число: "))
                num2 = float(input("Введите второе число: "))
                if operation == '+':
                    result = num1 + num2
                elif operation == '-':
                    result = num1 - num2
                elif operation == '*':
                    result = num1 * num2
                elif operation == '/':
                    result = num1 / num2
                elif operation == '**':
                    result = num1 ** num2
            
            print(f"Результат: {result}")
            save_calculation(operation, num1, num2 if operation != 'sqrt' else None, result)
        else:
            print("Неверная операция.")

def save_calculation(operation, num1, num2, result):
    calculation = {
        "operation": operation,
        "num1": num1,
        "num2": num2,
        "result": result
    }
    with open(CALC_HISTORY_FILE, 'r+') as f:
        history = json.load(f)
        history.append(calculation)
        f.seek(0)
        json.dump(history, f, indent=4)

def main():
    init_files()
    while True:
        choice = input("\n1. Регистрация\n2. Авторизация\n3. Выход\nВыберите опцию: ")
        if choice == '1':
            threading.Thread(target=register).start()
        elif choice == '2':
            username = login()
            if username:
                calculate()
        elif choice == '3':
            break
        else:
            print("Неверный выбор. Попробуйте снова.")

if __name__ == '__main__':
    main()

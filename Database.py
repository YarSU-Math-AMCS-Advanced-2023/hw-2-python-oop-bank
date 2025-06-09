import sqlite3

class Database:
    @staticmethod
    def create_db():
        # Создание или подключение к базе данных
        conn = sqlite3.connect("bank.db")

        # Создание курсора для выполнения SQL-запросов
        cursor = conn.cursor()

        # Создание таблицы пользователей, если она еще не существует
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            password TEXT NOT NULL  
        ) 
        ''')

        # Создание таблицы для хранения банковских карт, если она еще не существует
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS bank_cards (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                card_number TEXT NOT NULL,
                balance INTEGER NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
            ''')

        # Сохранение изменений и закрытие соединения
        conn.commit()
        conn.close()

    @staticmethod
    def add_user(name, password):
        # Создание или подключение к базе данных
        conn = sqlite3.connect("bank.db")

        # Создание курсора для выполнения SQL-запросов
        cursor = conn.cursor()

        # Добавление пользователя в таблицу
        cursor.execute('''
            INSERT INTO users (name, password)
            VALUES (?, ?)
        ''', (name, password))

        # Сохранение изменений и закрытие соединения
        conn.commit()
        conn.close()

    @staticmethod
    def get_user_id(name, password):
        # Подключение к базе данных
        conn = sqlite3.connect('bank.db')

        # Создание курсора для выполнения SQL-запросов
        cursor = conn.cursor()

        # Получение ID пользователя по имени и паролю
        cursor.execute('''
        SELECT id FROM users WHERE name = ? AND password = ?
        ''', (name, password))

        # Получение результата
        result = cursor.fetchone()

        # Закрытие соединения
        conn.close()

        # Если пользователь найден, возвращаем его ID, иначе - None
        return result[0] if result else None

    @staticmethod
    def show_users():
        # Подключение к базе данных
        conn = sqlite3.connect('bank.db')

        # Создание курсора для выполнения SQL-запросов
        cursor = conn.cursor()

        cursor.execute('''
        SELECT * FROM users
        ''')

        # Получение результата
        result = cursor.fetchall()

        # Закрытие соединения
        conn.close()

        # Если есть пользователи, возвращаем информацию, иначе None
        return result if result else None

    @staticmethod
    def create_card(user_id, card_number, balance):
        conn = sqlite3.connect("bank.db")
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO bank_cards (user_id, card_number, balance)
            VALUES(?, ?, ?)
        ''', (user_id, card_number, balance))

        conn.commit()
        conn.close()

    @staticmethod
    def get_cards(user_id):
        conn = sqlite3.connect("bank.db")
        cursor = conn.cursor()

        cursor.execute('''
            SELECT * FROM bank_cards WHERE user_id = ?
        ''', (user_id,))

        result = cursor.fetchall()

        conn.close()

        return result if result else None

    @staticmethod
    def get_balance(card_number):
        conn = sqlite3.connect("bank.db")
        cursor = conn.cursor()

        cursor.execute('''
                    SELECT balance FROM bank_cards WHERE card_number = ?
                ''', (card_number,))

        result = cursor.fetchone()

        conn.close()

        return result if result else None

    @staticmethod
    def get_card(card_number):
        conn = sqlite3.connect("bank.db")
        cursor = conn.cursor()

        cursor.execute('''
                            SELECT * FROM bank_cards WHERE card_number = ?
                        ''', (card_number,))

        result = cursor.fetchone()

        conn.close()

        return result if result else None

    @staticmethod
    def update_balance(card_number, new_balance):
        conn = sqlite3.connect("bank.db")
        cursor = conn.cursor()

        # SQL-запрос для обновления баланса карты
        cursor.execute('''
                UPDATE bank_cards
                SET balance = ?
                WHERE card_number = ?
            ''', (new_balance, card_number))

        conn.commit()
        conn.close()
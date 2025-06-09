import random
from database.Database import Database

class Bank:
    @staticmethod
    def create_storage():
        Database.create_db()

    @staticmethod
    def login(username, password):
        print(f'login with username: {username} and password: {password}')
        return Database.get_user_id(username, password)

    @staticmethod
    def registration(username, password):
        print(f'registration with username: {username} and password: {password}')
        Database.add_user(username, password)
        print(Database.show_users())

    @staticmethod
    def generate_card_number():
        # Генерируем первые 15 цифр номера карты
        card_number = [random.randint(0, 9) for _ in range(15)]

        # Применяем Лунный алгоритм для вычисления контрольной цифры
        def luhn_checksum(card_number):
            def digits_of(n):
                return [int(d) for d in str(n)]

            digits = digits_of(''.join(map(str, card_number)))
            odd_digits = digits[-1::-2]
            even_digits = digits[-2::-2]
            checksum = sum(odd_digits)
            for d in even_digits:
                checksum += sum(digits_of(d * 2))
            return checksum % 10

        # Находим контрольную цифру
        checksum = luhn_checksum(card_number)
        card_number.append((10 - checksum) % 10)

        return ''.join(map(str, card_number))

    @staticmethod
    def add_new_card(user_id):
        print(f'add card for user: {user_id}')
        new_card_number = Bank.generate_card_number()
        Database.create_card(user_id, new_card_number, 1000)

    @staticmethod
    def get_cards(user_id):
        print(f'get cards for user: {user_id}')
        return Database.get_cards(user_id)

    @staticmethod
    def get_balance(card_number):
        return Database.get_balance(card_number)

    @staticmethod
    def execute_transfer(card_number, target_card_number, sum):
        current_balance = Database.get_balance(card_number)[0]
        if current_balance < sum:
            return [False, "Недостаточно средств"]
        target_card = Database.get_card(target_card_number)
        if target_card is None:
            return [False, "Неверный номер карты получателя"]

        Database.update_balance(card_number, Bank.calculate_balance(current_balance, -sum))
        Database.update_balance(target_card_number, Bank.calculate_balance(target_card[3], sum))

        return [True, "Перевод совершён"]

    @staticmethod
    def add_money(card_number, sum):
        current_balance = Database.get_balance(card_number)[0]
        Database.update_balance(card_number, Bank.calculate_balance(current_balance, sum))

    @staticmethod
    def calculate_balance(current_balance, sum):
        return current_balance + sum
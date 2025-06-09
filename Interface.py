import flet as ft
from bank.Bank import Bank

class Interface:
    def __init__(self):
        Bank.create_storage()
        ft.app(target=self.login_form)

    # Создание окна авторизации
    def login_form(self, page: ft.Page):
        # Очистка текущей страницы
        page.controls.clear()
        # Заголовок страницы
        page.title = "Простой интерфейс с полями ввода"

        # Создание текстовых полей для ввода имени и пароля
        name_input = ft.TextField(label="Имя пользователя", width=300)
        password_input = ft.TextField(label="Пароль", password=True, width=300)

        # Кнопка для отправки данных
        login_button = ft.ElevatedButton("Отправить", on_click=lambda e: self.login(e, name_input.value, password_input.value, page))
        register_button = ft.ElevatedButton("Регистрация", on_click=lambda e: self.registration(e, name_input.value, password_input.value))

        form_column = ft.Column([
            name_input,
            password_input,
            login_button,
            register_button
        ], alignment=ft.MainAxisAlignment.CENTER)

        # Добавление элементов на страницу
        page.add(form_column)

    # Авторизация в банке
    def login(self, e, username, password, page):
        user_id = Bank.login(username, password)
        if (user_id is not None):
            self.user_id = user_id
            self.cabinet(page)

    # Регистрация в банке
    def registration(self, e, username, password):
        Bank.registration(username, password)

    def cabinet(self, page):
        # Очистка текущей страницы
        page.controls.clear()
        page.title = "Кабинет пользователя"

        # Добавление элементов на новую страницу
        page.add(ft.Text(f"Добро пожаловать в ваш кабинет, пользователь ID: {self.user_id}"))

        cards = Bank.get_cards(self.user_id)
        if (cards is not None):
            # Создание списка карт с кнопками
            for card in cards:
                card_id, user_id, card_number, balance = card

                # Добавление информации о карте
                card_info = ft.Column([
                    ft.Text(f"Карта ID: {card_id}"),
                    ft.Text(f"Номер карты: {card_number}"),
                    ft.Text(f"Баланс: {balance} рублей"),
                    ft.Row([
                        ft.ElevatedButton("Перевести", on_click=lambda e, cn=card_number: self.transfer(page, cn)),
                        ft.ElevatedButton("Пополнить", on_click=lambda e, cn=card_number: self.replenish(page, cn))
                    ])
                ])
                page.add(card_info)

        # Кнопка для возврата на страницу авторизации
        back_button = ft.ElevatedButton("Выйти", on_click=lambda e: self.login_form(page))
        add_card_button = ft.ElevatedButton("Создать счет", on_click=lambda e: self.create_card(page))
        page.add(back_button, add_card_button)

    def transfer(self, page, card_number):
        # Очистка текущих элементов на странице
        page.controls.clear()
        page.title = "Перевод средств"

        # Поля для ввода суммы и номера карты
        amount_input = ft.TextField(label="Сумма перевода", keyboard_type=ft.KeyboardType.NUMBER)
        target_card_input = ft.TextField(label="Номер карты получателя")

        # Кнопка для выполнения перевода
        transfer_button = ft.ElevatedButton("Перевести", on_click=lambda e: self.execute_transfer(page, card_number,
                                                                                                  target_card_input.value,
                                                                                                  amount_input.value))

        # Кнопка для отмены
        cancel_button = ft.ElevatedButton("Отмена", on_click=lambda e: self.cabinet(page))

        # Центрируем элементы на странице
        form_column = ft.Column([
            amount_input,
            target_card_input,
            transfer_button,
            cancel_button
        ], alignment=ft.MainAxisAlignment.CENTER)

        page.add(form_column)

    def execute_transfer(self, page, card_number, target_card_number, sum):
        status = Bank.execute_transfer(card_number, target_card_number, int(sum))
        if status[0]:
            self.cabinet(page)
        else:
            print(status[1])

    def replenish(self, page, card_number):
        # Очистка текущих элементов на странице
        page.controls.clear()
        page.title = "Пополнение счета"

        # Поля для ввода суммы и номера карты
        amount_input = ft.TextField(label="Сумма к пополнению", keyboard_type=ft.KeyboardType.NUMBER)

        # Кнопка пополнения
        add_money_button = ft.ElevatedButton("Пополнить", on_click=lambda e: self.execute_add_money(page, card_number, amount_input.value))

        # Кнопка для отмены
        cancel_button = ft.ElevatedButton("Отмена", on_click=lambda e: self.cabinet(page))

        # Центрируем элементы на странице
        form_column = ft.Column([
            amount_input,
            add_money_button,
            cancel_button
        ], alignment=ft.MainAxisAlignment.CENTER)

        page.add(form_column)

    def execute_add_money(self, page, card_number, sum):
        Bank.add_money(card_number, int(sum))
        self.cabinet(page)
    def create_card(self, page):
        Bank.add_new_card(self.user_id)
        self.cabinet(page)

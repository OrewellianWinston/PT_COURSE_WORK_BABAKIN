class IView:
    """
    Интерфейс представления (View).
    """
    def show_menu(self):
        pass

    def get_input(self, prompt: str) -> str:
        pass

    def show_message(self, message: str):
        pass

    def show_error(self, message: str):
        pass


class ConsoleView(IView):
    """
    Реализация View через консоль.
    """
    def show_menu(self):
        print("\n=== Меню ===")
        print("1. Добавить сотрудника")
        print("2. Добавить начисление")
        print("3. Посчитать годовую зарплату сотрудника")
        print("4. Показать статистику (сум, сред, макс, мин)")
        print("0. Выход")

    def get_input(self, prompt: str) -> str:
        return input(prompt)

    def show_message(self, message: str):
        print(message)

    def show_error(self, message: str):
        print(f"ОШИБКА: {message}")

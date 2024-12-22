from decimal import Decimal
from datetime import datetime
from model import EmployeeFactory, PayrollItem
from view import IView

class AppPresenter:
    def __init__(self, view: IView):
        self.view = view
        # Храним сотрудников в памяти (список), без БД
        self.employees = []

    def run(self):
        """
        Основной цикл приложения: показываем меню,
        обрабатываем выбор пользователя.
        """
        while True:
            self.view.show_menu()
            choice = self.view.get_input("Выберите пункт меню: ")

            if choice == "1":
                self.add_employee()
            elif choice == "2":
                self.add_payroll_item()
            elif choice == "3":
                self.calculate_annual_salary()
            elif choice == "4":
                self.show_statistics()
            elif choice == "0":
                self.view.show_message("До свидания!")
                break
            else:
                self.view.show_error("Неверный пункт меню")

    def add_employee(self):
        """
        Добавляем сотрудника:
        Запрашиваем тип, имя, должность, необходимые ставки.
        """
        emp_type = self.view.get_input("Тип сотрудника (fixed/hourly/commission): ")
        full_name = self.view.get_input("ФИО: ")
        position = self.view.get_input("Должность: ")

        # в зависимости от типа - запрашиваем разные поля
        if emp_type == "fixed":
            rate_str = self.view.get_input("Месячная ставка: ")
            rate = Decimal(rate_str)
            emp = EmployeeFactory.create_employee(
                employee_type='fixed',
                full_name=full_name,
                position=position,
                rate=rate
            )
        elif emp_type == "hourly":
            hour_rate_str = self.view.get_input("Ставка в час: ")
            hours_per_month_str = self.view.get_input("Часов в месяц: ")
            hour_rate = Decimal(hour_rate_str)
            hours_per_month = int(hours_per_month_str)
            emp = EmployeeFactory.create_employee(
                employee_type='hourly',
                full_name=full_name,
                position=position,
                hour_rate=hour_rate,
                hours_per_month=hours_per_month
            )
        elif emp_type == "commission":
            base_str = self.view.get_input("Базовая ставка в месяц: ")
            comm_str = self.view.get_input("Процент комиссии (число): ")
            base_rate = Decimal(base_str)
            commission_percent = Decimal(comm_str)
            emp = EmployeeFactory.create_employee(
                employee_type='commission',
                full_name=full_name,
                position=position,
                base_rate=base_rate,
                commission_percent=commission_percent
            )
        else:
            self.view.show_error("Неизвестный тип!")
            return

        self.employees.append(emp)
        self.view.show_message(f"Сотрудник {emp.full_name} добавлен!")

    def add_payroll_item(self):
        """
        Добавить начисление к сотруднику
        """
        if not self.employees:
            self.view.show_error("Нет сотрудников!")
            return

        # Выведем список сотрудников
        for i, emp in enumerate(self.employees):
            self.view.show_message(f"[{i}] {emp.full_name} ({emp.employee_type})")

        idx_str = self.view.get_input("Выберите индекс сотрудника: ")
        try:
            idx = int(idx_str)
            employee = self.employees[idx]
        except (ValueError, IndexError):
            self.view.show_error("Некорректный индекс!")
            return

        desc = self.view.get_input("Описание начисления: ")
        amt_str = self.view.get_input("Сумма начисления: ")
        date_str = self.view.get_input("Дата (YYYY-MM-DD): ")

        try:
            amount = Decimal(amt_str)
            pay_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except Exception as e:
            self.view.show_error(f"Ошибка при вводе: {e}")
            return

        item = PayrollItem(description=desc, amount=amount, date=pay_date)
        employee.add_payroll_item(item)
        self.view.show_message(f"Начисление добавлено сотруднику {employee.full_name}.")

    def calculate_annual_salary(self):
        """
        Посчитать годовую зарплату конкретного сотрудника за год.
        """
        if not self.employees:
            self.view.show_error("Нет сотрудников!")
            return

        # список сотрудников
        for i, emp in enumerate(self.employees):
            self.view.show_message(f"[{i}] {emp.full_name}")

        idx_str = self.view.get_input("Выберите индекс сотрудника: ")
        year_str = self.view.get_input("Введите год (например, 2024): ")

        try:
            idx = int(idx_str)
            year = int(year_str)
            employee = self.employees[idx]
        except (ValueError, IndexError):
            self.view.show_error("Некорректный ввод!")
            return

        annual_salary = employee.get_annual_salary(year)
        self.view.show_message(
            f"Годовая зарплата {employee.full_name} за {year} = {annual_salary}"
        )

    def show_statistics(self):
        """
        Показать агрегирующую статистику по всем сотрудникам
        (сумма, среднее, макс, мин).
        """
        if not self.employees:
            self.view.show_error("Нет сотрудников!")
            return

        year_str = self.view.get_input("Введите год (например, 2024): ")
        try:
            year = int(year_str)
        except ValueError:
            self.view.show_error("Неверный год!")
            return

        salaries = []
        for emp in self.employees:
            sal = emp.get_annual_salary(year)
            salaries.append(sal)

        if not salaries:
            self.view.show_message("Нет начислений за указанный год.")
            return

        total_sum = sum(salaries)
        avg_salary = total_sum / len(salaries)
        max_salary = max(salaries)
        min_salary = min(salaries)

        self.view.show_message("Статистика:")
        self.view.show_message(f"  Суммарная зарплата: {total_sum}")
        self.view.show_message(f"  Средняя зарплата:   {avg_salary}")
        self.view.show_message(f"  Максимальная:       {max_salary}")
        self.view.show_message(f"  Минимальная:        {min_salary}")

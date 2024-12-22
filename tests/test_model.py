import unittest
from decimal import Decimal
from datetime import date
from model import EmployeeFactory, PayrollItem


class TestEmployeeModel(unittest.TestCase):
    def test_fixed_salary_employee(self):
        """
        Проверим сотрудника с 'штатным' типом оплаты
        (месячный оклад).
        """
        emp = EmployeeFactory.create_employee(
            employee_type='штатный',
            full_name='Иванов Иван',
            position='Инженер',
            monthly_rate=Decimal(1000)
        )
        # Добавим пару начислений
        emp.add_payroll_item(PayrollItem("Премия", Decimal(500), date(2024, 5, 10)))
        emp.add_payroll_item(PayrollItem("Сверхурочная", Decimal(300), date(2023, 12, 25)))  # Др. год

        # За 2024 год: оклад = 1000*12=12000 + премия=500 => 12500
        self.assertEqual(emp.get_annual_salary(2024), Decimal(12500))

        # За 2023 год: только "Сверхурочная" 300 + оклад 1000*12=12000 => 12300
        self.assertEqual(emp.get_annual_salary(2023), Decimal(12300))

    def test_hourly_salary_employee(self):
        """
        Проверим сотрудника 'почасовой'.
        """
        emp = EmployeeFactory.create_employee(
            employee_type='почасовой',
            full_name='Петров Петр',
            position='Разработчик',
            hour_rate=Decimal("100.50"),
            hours_per_month=160
        )
        emp.add_payroll_item(PayrollItem("Премия", Decimal(1000), date(2024, 1, 15)))

        # Базовый оклад: 100.50 * 160 * 12 = 100.50 * 1920 = 192960
        # Плюс премия 1000
        self.assertEqual(emp.get_annual_salary(2024), Decimal("193960"))

    def test_commission_employee(self):
        """
        Проверим 'с_комиссией' тип: base_rate + комиссия.
        """
        emp = EmployeeFactory.create_employee(
            employee_type='с_комиссией',
            full_name='Сидоров Сидр',
            position='Менеджер по продажам',
            base_rate=Decimal(500),
            commission_percent=Decimal(10)
        )
        # base_rate=500 означает 500 руб./мес
        # за 12 мес: 6000
        # комиссия 10% = 600 (от 6000)
        # Итого 6600
        # + начисления
        emp.add_payroll_item(PayrollItem("Бонус за проект", Decimal(2000), date(2024, 6, 1)))

        # Ожидаем 6600 + 2000 = 8600
        self.assertEqual(emp.get_annual_salary(2024), Decimal(8600))

        # За другой год (допустим, 2023) — без начислений, только 6600
        self.assertEqual(emp.get_annual_salary(2023), Decimal(6600))


if __name__ == '__main__':
    unittest.main()

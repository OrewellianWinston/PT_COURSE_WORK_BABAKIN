import unittest
from decimal import Decimal
from datetime import date
from model import EmployeeFactory, PayrollItem
from services import calculate_statistics

class TestServices(unittest.TestCase):
    def test_calculate_statistics(self):
        emp1 = EmployeeFactory.create_employee(
            'штатный',
            'Иванов Иван',
            'Инженер',
            monthly_rate=Decimal(1000)
        )
        emp1.add_payroll_item(PayrollItem("Премия", Decimal(500), date(2024, 5, 10)))

        emp2 = EmployeeFactory.create_employee(
            'почасовой',
            'Петров Петр',
            'Разработчик',
            hour_rate=Decimal("100.5"),
            hours_per_month=160
        )
        emp2.add_payroll_item(PayrollItem("Бонус", Decimal(1000), date(2024, 1, 15)))

        employees = [emp1, emp2]
        stats_2024 = calculate_statistics(employees, 2024)

        # Посчитаем вручную:
        # emp1 -> 1000*12 + 500 = 12500
        # emp2 -> (100.5 *160*12) +1000 = 193960
        # sum = 12500+193960=206460
        # avg=206460/2=103230
        # max=193960, min=12500
        self.assertEqual(stats_2024['sum'], Decimal("206460"))
        self.assertEqual(stats_2024['avg'], Decimal("103230"))
        self.assertEqual(stats_2024['max'], Decimal("193960"))
        self.assertEqual(stats_2024['min'], Decimal("12500"))

if __name__ == '__main__':
    unittest.main()

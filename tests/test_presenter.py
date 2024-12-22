import unittest
from unittest.mock import MagicMock
from decimal import Decimal
from presenter import AppPresenter
from model import Employee


class TestPresenter(unittest.TestCase):
    def test_add_employee_fixed(self):
        # Создадим мок для view
        mock_view = MagicMock()
        presenter = AppPresenter(mock_view)

        # Настроим последовательность возврата от get_input():
        # 1) "штатный"
        # 2) "Иванов Иван"
        # 3) "Инженер"
        # 4) "1000" (месячная ставка)
        mock_view.get_input.side_effect = [
            "штатный",
            "Иванов Иван",
            "Инженер",
            "1000"
        ]

        presenter.add_employee()

        self.assertEqual(len(presenter.employees), 1)
        emp = presenter.employees[0]
        self.assertIsInstance(emp, Employee)
        self.assertEqual(emp.full_name, "Иванов Иван")
        self.assertEqual(emp.monthly_rate, Decimal("1000"))

        # Проверим, что mock_view.show_message() вызывался
        mock_view.show_message.assert_called_with("Сотрудник Иванов Иван добавлен!")


if __name__ == '__main__':
    unittest.main()

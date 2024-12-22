from typing import List, Optional
from decimal import Decimal
from datetime import date

class Employee:
    """
    Базовый класс Сотрудника.
    Пример: employee_type может быть 'fixed', 'hourly', 'commission'.
    """
    def __init__(self, full_name: str, position: str, employee_type: str,
                 monthly_rate: Optional[Decimal] = None,
                 hour_rate: Optional[Decimal] = None,
                 hours_per_month: Optional[int] = None,
                 base_rate: Optional[Decimal] = None,
                 commission_percent: Optional[Decimal] = None):
        self.full_name = full_name
        self.position = position
        self.employee_type = employee_type  # 'fixed', 'hourly', 'commission'

        self.monthly_rate = monthly_rate
        self.hour_rate = hour_rate
        self.hours_per_month = hours_per_month
        self.base_rate = base_rate
        self.commission_percent = commission_percent

        self.payroll_items: List[PayrollItem] = []

    def add_payroll_item(self, item: "PayrollItem"):
        self.payroll_items.append(item)

    def get_annual_salary(self, year: int = 2024) -> Decimal:
        """
        Пример простейшего расчёта:
          - 'fixed': monthly_rate * 12
          - 'hourly': hour_rate * hours_per_month * 12
          - 'commission': (base_rate * 12) + (commission_percent% от base?) + ...
        Плюс суммируем все PayrollItem за нужный год.
        """
        payroll_sum = Decimal(0)
        for item in self.payroll_items:
            if item.date.year == year:
                payroll_sum += item.amount

        if self.employee_type == 'fixed':
            base = (self.monthly_rate or Decimal(0)) * Decimal(12)
            return base + payroll_sum

        elif self.employee_type == 'hourly':
            base = (self.hour_rate or Decimal(0)) * (Decimal(self.hours_per_month or 0)) * Decimal(12)
            return base + payroll_sum

        elif self.employee_type == 'commission':
            base = (self.base_rate or Decimal(0)) * Decimal(12)
            commission = base * ((self.commission_percent or Decimal(0)) / Decimal(100))
            return base + commission + payroll_sum

        # если неизвестный тип
        return payroll_sum


class PayrollItem:
    """
    Класс, описывающий дополнительное начисление (премия, надбавка и т.д.)
    """
    def __init__(self, description: str, amount: Decimal, date: date):
        self.description = description
        self.amount = amount
        self.date = date

    def __repr__(self):
        return f"PayrollItem(desc={self.description}, amount={self.amount}, date={self.date})"


class EmployeeFactory:
    """
    Простейшая фабрика для создания Employee по типу ('fixed', 'hourly', 'commission').
    """
    @staticmethod
    def create_employee(employee_type: str, full_name: str, position: str,
                        rate: Decimal = Decimal(0),
                        hour_rate: Decimal = Decimal(0),
                        hours_per_month: int = 0,
                        base_rate: Decimal = Decimal(0),
                        commission_percent: Decimal = Decimal(0)) -> Employee:

        if employee_type == 'fixed':
            return Employee(
                full_name=full_name,
                position=position,
                employee_type='fixed',
                monthly_rate=rate
            )
        elif employee_type == 'hourly':
            return Employee(
                full_name=full_name,
                position=position,
                employee_type='hourly',
                hour_rate=hour_rate,
                hours_per_month=hours_per_month
            )
        elif employee_type == 'commission':
            return Employee(
                full_name=full_name,
                position=position,
                employee_type='commission',
                base_rate=base_rate,
                commission_percent=commission_percent
            )
        else:
            raise ValueError(f"Неизвестный тип сотрудника: {employee_type}")

from typing import List, Optional
from decimal import Decimal
from datetime import date

from strategy import (
    ISalaryCalcStrategy,
    FixedSalaryStrategy,
    HourlySalaryStrategy,
    CommissionSalaryStrategy
)


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


class Employee:
    """
    Теперь Employee хранит только поля + стратегию расчёта з/п.
    """
    def __init__(self,
                 full_name: str,
                 position: str,
                 strategy: ISalaryCalcStrategy,
                 monthly_rate: Optional[Decimal] = None,
                 hour_rate: Optional[Decimal] = None,
                 hours_per_month: Optional[int] = None,
                 base_rate: Optional[Decimal] = None,
                 commission_percent: Optional[Decimal] = None):

        self.full_name = full_name
        self.position = position
        self.strategy = strategy  # ссылка на объект, реализующий ISalaryCalcStrategy

        self.monthly_rate = monthly_rate
        self.hour_rate = hour_rate
        self.hours_per_month = hours_per_month
        self.base_rate = base_rate
        self.commission_percent = commission_percent

        self.payroll_items: List[PayrollItem] = []

    def add_payroll_item(self, item: PayrollItem):
        self.payroll_items.append(item)

    def get_payroll_sum_for_year(self, year: int) -> Decimal:
        total = Decimal(0)
        for item in self.payroll_items:
            if item.date.year == year:
                total += item.amount
        return total

    def get_annual_salary(self, year: int) -> Decimal:
        return self.strategy.calculate_annual_salary(self, year)


class EmployeeFactory:
    """
    Обновим фабрику: в зависимости от типа сотрудника - подставим нужную стратегию.
    employee_type: 'штатный', 'почасовой', 'с_комиссией'
    """
    @staticmethod
    def create_employee(employee_type: str,
                        full_name: str,
                        position: str,
                        monthly_rate: Decimal = Decimal(0),
                        hour_rate: Decimal = Decimal(0),
                        hours_per_month: int = 0,
                        base_rate: Decimal = Decimal(0),
                        commission_percent: Decimal = Decimal(0)
                        ) -> Employee:

        if employee_type == 'штатный':
            strategy = FixedSalaryStrategy()
            return Employee(
                full_name=full_name,
                position=position,
                strategy=strategy,
                monthly_rate=monthly_rate
            )
        elif employee_type == 'почасовой':
            strategy = HourlySalaryStrategy()
            return Employee(
                full_name=full_name,
                position=position,
                strategy=strategy,
                hour_rate=hour_rate,
                hours_per_month=hours_per_month
            )
        elif employee_type == 'с_комиссией':
            strategy = CommissionSalaryStrategy()
            return Employee(
                full_name=full_name,
                position=position,
                strategy=strategy,
                base_rate=base_rate,
                commission_percent=commission_percent
            )
        else:
            raise ValueError(f"Неизвестный тип сотрудника: {employee_type}")

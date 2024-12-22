from abc import ABC, abstractmethod
from decimal import Decimal
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from model import Employee

class ISalaryCalcStrategy(ABC):
    """
    Интерфейс / абстрактный класс для расчёта годовой зарплаты.
    """
    @abstractmethod
    def calculate_annual_salary(self, employee: "Employee", year: int) -> Decimal:
        pass


class FixedSalaryStrategy(ISalaryCalcStrategy):
    def calculate_annual_salary(self, employee: "Employee", year: int) -> Decimal:
        from decimal import Decimal
        payroll_sum = employee.get_payroll_sum_for_year(year)
        monthly_rate = employee.monthly_rate or Decimal(0)
        return monthly_rate * Decimal(12) + payroll_sum


class HourlySalaryStrategy(ISalaryCalcStrategy):
    def calculate_annual_salary(self, employee: "Employee", year: int) -> Decimal:
        payroll_sum = employee.get_payroll_sum_for_year(year)
        hour_rate = employee.hour_rate or Decimal(0)
        hours_per_month = employee.hours_per_month or 0
        return hour_rate * hours_per_month * Decimal(12) + payroll_sum


class CommissionSalaryStrategy(ISalaryCalcStrategy):
    def calculate_annual_salary(self, employee: "Employee", year: int) -> Decimal:
        payroll_sum = employee.get_payroll_sum_for_year(year)
        base = (employee.base_rate or Decimal(0)) * Decimal(12)
        commission = base * ((employee.commission_percent or Decimal(0)) / Decimal(100))
        return base + commission + payroll_sum

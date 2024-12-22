from typing import List
from decimal import Decimal
from model import Employee

def calculate_annual_salary(employee: Employee, year: int) -> Decimal:
    """
    Обёртка (хотя можно вызывать и напрямую employee.get_annual_salary).
    Но, к примеру, сюда можно добавить ещё какую-то логику логгирования, кэширования и т.п.
    """
    return employee.get_annual_salary(year)


def calculate_statistics(employees: List[Employee], year: int):
    """
    Считает сумму, среднее, макс, мин.
    Возвращает словарь или кортеж, как удобнее.
    """
    if not employees:
        return {"sum": 0, "avg": 0, "max": 0, "min": 0}

    salaries = [emp.get_annual_salary(year) for emp in employees]

    if not salaries:
        return {"sum": 0, "avg": 0, "max": 0, "min": 0}

    total_sum = sum(salaries)
    avg_salary = total_sum / len(salaries)
    max_salary = max(salaries)
    min_salary = min(salaries)

    return {
        "sum": total_sum,
        "avg": avg_salary,
        "max": max_salary,
        "min": min_salary
    }

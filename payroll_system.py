from datetime import datetime
from abc import ABC, abstractmethod
from typing import Dict, List

# ---------------- Employees ---------------- #

class Employee(ABC):
    def __init__(self, name, department):
        self.name = name
        self._department = department

    @abstractmethod
    def calculate_pay(self, period_hours=None):
        pass

    def __str__(self):
        return f"{self.name} ({self._department})"


class SalariedEmployee(Employee):
    def __init__(self, name, department, monthly_salary=0):
        super().__init__(name, department)
        self.__monthly_salary = 0.0
        self.monthly_salary = monthly_salary

    @property
    def monthly_salary(self):
        return self.__monthly_salary

    @monthly_salary.setter
    def monthly_salary(self, value):
        if not isinstance(value, (int, float)) or value < 0:
            raise ValueError("monthly_salary must be a non-negative number.")
        self.__monthly_salary = float(value)

    def calculate_pay(self, period_hours=None):
        return float(self.__monthly_salary)

    def apply_raise(self, percent):
        if not isinstance(percent, (int, float)):
            raise ValueError("percent must be a number.")
        new_salary = self.__monthly_salary * (1 + percent / 100.0)
        if new_salary < 0:
            raise ValueError("Resulting salary cannot be negative.")
        self.__monthly_salary = new_salary


class HourlyEmployee(Employee):
    def __init__(self, name, department, hourly_rate):
        super().__init__(name, department)
        if hourly_rate < 0:
            raise ValueError("hourly_rate must be non-negative.")
        self.hourly_rate = float(hourly_rate)
        self.__overtime_multiplier = 1.5

    def calculate_pay(self, period_hours=None):
        if period_hours is None or period_hours < 0:
            raise ValueError("period_hours must be provided and non-negative.")
        base_hours = min(period_hours, 160)
        overtime_hours = max(period_hours - 160, 0)
        return base_hours * self.hourly_rate + overtime_hours * self.hourly_rate * self.__overtime_multiplier

    def set_overtime_multiplier(self, x):
        if not isinstance(x, (int, float)) or x < 1.0:
            raise ValueError("Overtime multiplier must be a number >= 1.0.")
        self.__overtime_multiplier = float(x)


class Contractor(Employee):
    def __init__(self, name, department, daily_rate):
        super().__init__(name, department)
        if daily_rate < 0:
            raise ValueError("daily_rate must be non-negative.")
        self.daily_rate = float(daily_rate)
        self.__days_worked = 0

    def log_day(self):
        self.__days_worked += 1

    def reset_days(self):
        self.__days_worked = 0

    def calculate_pay(self, period_hours=None):
        return self.daily_rate * self.__days_worked


# ---------------- Utilities ---------------- #

class Logger:
    def log(self, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"{timestamp}  {message}")


class FileLogger(Logger):
    def __init__(self, path="payroll.log", encoding="utf-8"):
        self.path = path
        self.encoding = encoding

    def log(self, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.path, "a", encoding=self.encoding, newline="") as f:
            f.write(f"{timestamp}  {message}\n")



def run_payroll(employees: List[Employee], period_hours_map: Dict[str, float]) -> Dict[str, float]:
    results: Dict[str, float] = {}
    for emp in employees:
        if isinstance(emp, HourlyEmployee):
            if emp.name not in period_hours_map:
                raise ValueError(f"Missing hours for hourly employee {emp.name}.")
            hours = period_hours_map[emp.name]
            pay = emp.calculate_pay(hours)
        else:
            pay = emp.calculate_pay()
        results[emp.name] = round(float(pay), 2)
    return results


# ---------------- Payments ---------------- #

class PaymentProcessor(ABC):
    @abstractmethod
    def pay(self, employee_name, amount):
        pass


class BankTransferProcessor(PaymentProcessor):
    def pay(self, employee_name, amount):
        print(f"Transferring {amount:.2f} MAD to {employee_name} via bank transfer...")


class CashProcessor(PaymentProcessor):
    def pay(self, employee_name, amount):
        print(f"Handing {amount:.2f} MAD cash to {employee_name}...")


# ---------------- Tax Calculation ---------------- #

class TaxCalculator:
    @staticmethod
    def net(amount: float) -> float:
        if amount <= 3000:
            return amount
        elif amount <= 10000:
            return amount * 0.90
        else:
            return amount * 0.80

    def compute_net_map(self, gross_map: Dict[str, float]) -> Dict[str, float]:
        return {name: round(self.net(gross), 2) for name, gross in gross_map.items()}


# ---------------- Orchestration ---------------- #

class PayrollSystem:
    def __init__(self, employees: List[Employee], payment_processor: PaymentProcessor, logger: Logger, tax_calculator: TaxCalculator | None = None):
        self.employees = employees
        self.payment_processor = payment_processor
        self.logger = logger
        self.tax_calculator = tax_calculator

    def process_payroll(self, period_hours_map: Dict[str, float]) -> Dict[str, float]:
        self.logger.log("Running payroll...")
        gross_map = run_payroll(self.employees, period_hours_map)

        if self.tax_calculator is not None:
            net_map = self.tax_calculator.compute_net_map(gross_map)
        else:
            net_map = gross_map

        for emp in self.employees:
            name = emp.name
            gross = gross_map[name]
            net = net_map[name]
            self.logger.log(f"Paying {name}: gross {gross:.2f} MAD → net {net:.2f} MAD")
            self.payment_processor.pay(name, net)

        self.logger.log("Payroll complete.")
        return net_map


# ---------------- Demo ---------------- #

if __name__ == "__main__":
    se = SalariedEmployee("Amina", "Finance", 12000)
    he = HourlyEmployee("Yassine", "IT", 80)         # 80 MAD/hour
    co = Contractor("Laila", "Marketing", 900)       # 900 MAD/day

    se.apply_raise(5)                         # +5% → 12600 gross
    co.log_day(); co.log_day(); co.log_day() # 3 days → 2700 gross
    he.set_overtime_multiplier(2.0)
    period_hours_map = {"Yassine": 172}      # 12 OT hours → 14720 gross

    tax = TaxCalculator()

    # Run with FileLogger
    file_logger = FileLogger("payroll.log")
    payroll_system = PayrollSystem([se, he, co], CashProcessor(), file_logger, tax)
    payroll_system.process_payroll(period_hours_map)

    print("✅ Payroll processed. Check payroll.log for details.")

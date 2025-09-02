# 🧾 Python Payroll Management System

A simple yet extensible **Payroll Management System** built in Python using **Object-Oriented Programming (OOP)**.

---

## 🚀 Features
- Manage multiple employee types:
  - **SalariedEmployee** → fixed monthly salary
  - **HourlyEmployee** → paid per hour + overtime multiplier
  - **Contractor** → paid per logged workdays
- Tax calculation with multiple brackets
- Apply raises and adjust overtime multiplier
- Multiple payment methods:
  - 💳 Bank Transfer
  - 💵 Cash
- Logging:
  - 📜 Console logs
  - 🗂️ File logs (`payroll.log`)
- Extensible architecture (easily add new employee types, payment processors, or tax rules)
---

## ⚙️ Installation

1. Clone the repo:
   ```bash
   git clone https://github.com/Sn4iZer/payroll-system.git
   cd payroll-system
   python payroll_system.py

💻 Example Usage
```bash
from payroll_system import (
    SalariedEmployee, HourlyEmployee, Contractor,
    CashProcessor, BankTransferProcessor,
    PayrollSystem, Logger, FileLogger
)
```
# Employees
```
se = SalariedEmployee("Amina", "Finance", 12000)

he = HourlyEmployee("Yassine", "IT", 80)

co = Contractor("Laila", "Marketing", 900)


se.apply_raise(5)        # +5%

he.set_overtime_multiplier(2.0)

co.log_day(); co.log_day(); co.log_day()
```

# Hours worked this month
```
period_hours_map = {"Yassine": 172}
```

# Run Payroll
```
logger = FileLogger("payroll.log")

system = PayrollSystem([se, he, co], BankTransferProcessor(), logger)

system.process_payroll(period_hours_map)
```
📊 Example Output
```
2025-09-01 10:12:23  Running payroll...

2025-09-01 10:12:23  Paying Amina: gross 12600.00 MAD → net 10080.00 MAD

2025-09-01 10:12:23  Paying Yassine: gross 14080.00 MAD → net 11264.00 MAD

2025-09-01 10:12:23  Paying Laila: gross 2700.00 MAD → net 2430.00 MAD

2025-09-01 10:12:23  Payroll complete.
```
## 🛠️ Future Improvements

- Add a Tkinter GUI Dashboard for payroll visualization
- Store employee & payroll data in a SQLite database
- Export reports to Excel / CSV
- Add authentication for HR/Admin users

## 👨‍💻 Author
SnaiZer

## 📜 License

This project is licensed under the MIT License.

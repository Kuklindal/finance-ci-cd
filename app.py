import json
import sys
from pathlib import Path

DATA_FILE = Path(__file__).with_name("transactions.json")


def add_transaction(transactions, kind, amount, description):
    if kind not in ("income", "expense"):
        raise ValueError("Тип должен быть income или expense")
    if type(amount) is not int or amount <= 0:
        raise ValueError("Сумма должна быть положительным целым числом")

    transactions.append({
        "kind": kind,
        "amount": amount,
        "description": description,
    })


def calculate_totals(transactions):
    incomes = sum(t["amount"] for t in transactions if t["kind"] == "income")
    expenses = sum(t["amount"] for t in transactions if t["kind"] == "expense")
    balance = incomes - expenses
    return incomes, expenses, balance


def load_transactions(path):
    if not path.exists():
        return []
    return json.loads(path.read_text(encoding="utf-8"))


def save_transactions(transactions, path):
    path.write_text(
        json.dumps(transactions, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def show_totals(transactions):
    incomes, expenses, balance = calculate_totals(transactions)
    print(f"Доходы: {incomes} руб.")
    print(f"Расходы: {expenses} руб.")
    print(f"Баланс: {balance} руб.")


def main():
    if len(sys.argv) == 2 and sys.argv[1] == "--demo":
        demo = []
        add_transaction(demo, "income", 80000, "Зарплата")
        add_transaction(demo, "expense", 25000, "Аренда")
        show_totals(demo)
        return

    transactions = load_transactions(DATA_FILE)
    while True:
        print("\n1 — Доход | 2 — Расход | 3 — Баланс | 0 — Выход")
        choice = input("Выбор: ").strip()

        if choice == "0":
            return
        if choice == "3":
            show_totals(transactions)
            continue
        if choice not in ("1", "2"):
            print("Неизвестная команда")
            continue

        try:
            amount = int(input("Сумма в рублях: "))
            description = input("Описание: ").strip()
            kind = "income" if choice == "1" else "expense"
            add_transaction(transactions, kind, amount, description)
        except ValueError as error:
            print(f"Ошибка ввода: {error}")
            continue

        save_transactions(transactions, DATA_FILE)
        print("Операция сохранена")


if __name__ == "__main__":
    main()

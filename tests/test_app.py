import pytest

from app import add_transaction, calculate_totals, load_transactions, save_transactions


def test_empty_list():
    assert calculate_totals([]) == (0, 0, 0)


def test_only_income():
    operations = []
    add_transaction(operations, "income", 80000, "Зарплата")
    assert calculate_totals(operations) == (80000, 0, 80000)


def test_expense_reduces_balance():
    operations = []
    add_transaction(operations, "income", 80000, "Зарплата")
    add_transaction(operations, "expense", 25000, "Аренда")
    assert calculate_totals(operations) == (80000, 25000, 55000)


def test_multiple_transactions():
    operations = []
    add_transaction(operations, "income", 80000, "Зарплата")
    add_transaction(operations, "income", 10000, "Подработка")
    add_transaction(operations, "expense", 25000, "Аренда")
    add_transaction(operations, "expense", 5000, "Продукты")
    assert calculate_totals(operations) == (90000, 30000, 60000)


def test_invalid_transaction_type():
    with pytest.raises(ValueError):
        add_transaction([], "transfer", 1000, "Перевод")


@pytest.mark.parametrize("bad_amount", [0, -100, 10.5])
def test_invalid_amount(bad_amount):
    with pytest.raises(ValueError):
        add_transaction([], "expense", bad_amount, "Ошибка")


def test_save_and_load(tmp_path):
    file_path = tmp_path / "operations.json"
    operations = []
    add_transaction(operations, "income", 5000, "Подарок")
    save_transactions(operations, file_path)
    assert load_transactions(file_path) == operations


def test_load_missing_file(tmp_path):
    assert load_transactions(tmp_path / "missing.json") == []

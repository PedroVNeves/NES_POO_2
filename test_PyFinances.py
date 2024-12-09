import pytest
from datetime import datetime
from PyFinances.finances import converter_para_datetime, calcular_meses_fechados, calcular_juros_compostos, Transaction, Account, Investment, Client

# Testes para converter_para_datetime
def test_converter_para_datetime_str():
    date_str = "08/12/2024"
    result = converter_para_datetime(date_str)
    assert result == datetime(2024, 12, 8), f"Expected datetime(2024, 12, 8), got {result}"

def test_converter_para_datetime_datetime():
    date_obj = datetime(2024, 12, 8)
    result = converter_para_datetime(date_obj)
    assert result == date_obj, f"Expected datetime(2024, 12, 8), got {result}"

def test_converter_para_datetime_invalid():
    with pytest.raises(ValueError, match="A string da data deve estar no formato 'dd/mm/yyyy'."):
        converter_para_datetime("08-12-2024")

# Testes para calcular_meses_fechados
def test_calcular_meses_fechados():
    data_inicial = "08/12/2023"
    data_final = "08/12/2024"
    result = calcular_meses_fechados(data_inicial, data_final)
    assert result == 12, f"Expected 12 months, got {result}"

def test_calcular_meses_fechados_dia_menor():
    data_inicial = "08/11/2024"
    data_final = "08/12/2024"
    result = calcular_meses_fechados(data_inicial, data_final)
    assert result == 1, f"Expected 1 month, got {result}"

# Testes para calcular_juros_compostos
def test_calcular_juros_compostos():
    principal = 1000
    taxa = 0.05
    data_inicio = "08/12/2023"
    data_final = "08/12/2024"
    result = calcular_juros_compostos(principal, taxa, data_inicio, data_final)
    assert result == 1795.86, f"Expected 1795.86, got {result}"

# Testes para Transaction
def test_transaction_str():
    transaction = Transaction(100.0, "08/12/2024", "Food", "Supermarket purchase")
    assert str(transaction) == "Supermarket purchase.R$100.0.Food ", f"Expected 'Supermarket purchase.R$100.0.Food ', got {str(transaction)}"

def test_transaction_update():
    transaction = Transaction(100.0, "08/12/2024", "Food", "Supermarket purchase")
    transaction.update("amount", 150.0)
    transaction.update("category", "Bills")
    transaction.update("description", "Electricity bill")
    assert str(transaction) == "Electricity bill.R$150.0.Bills ", f"Expected 'Electricity bill.R$150.0.Bills ', got {str(transaction)}"

# Testes para Account
def test_account_add_transaction():
    client = Client("Test Client")
    account = Account("Test Account", 500.0, client)
    account.add_transaction(200.0, "08/12/2024", "Income", "Salary")
    assert account.balance == 700.0, f"Expected balance 700.0, got {account.balance}"
    assert len(account.transactions) == 1, f"Expected 1 transaction, got {len(account.transactions)}"

def test_account_get_transactions():
    client = Client("Test Client")
    account = Account("Test Account", 500.0, client)
    account.add_transaction(200.0, "08/12/2024", "Income", "Salary")
    account.add_transaction(-50.0, "08/12/2024", "Expense", "Electricity bill")
    transactions = account.get_transactions("08/12/2024", "08/12/2024")
    assert len(transactions) == 2, f"Expected 2 transactions, got {len(transactions)}"

# Testes para Investment
def test_investment_calculate_value():
    client = Client("Test Client")
    investment = Investment("ações", 1000.0, "08/12/2023", 0.05, client)
    result = investment.calculate_value("08/12/2024")
    assert result == 1795.86, f"Expected 1795.86, got {result}"
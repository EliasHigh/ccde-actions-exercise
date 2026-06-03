import unittest
from app.bank_account import BankAccount


class TestBankAccount(unittest.TestCase):
    def setUp(self):
        self.account = BankAccount("Max Mustermann", 100.0)

    def test_initial_balance(self):
        self.assertEqual(self.account.get_balance(), 100.0)

    def test_initial_balance_zero(self):
        account = BankAccount("Test User")
        self.assertEqual(account.get_balance(), 0.0)

    def test_negative_initial_balance_raises(self):
        with self.assertRaises(ValueError):
            BankAccount("Test", -50.0)

    def test_deposit_adds_to_balance(self):
        self.account.deposit(50.0)
        self.assertEqual(self.account.get_balance(), 150.0)

    def test_deposit_zero_raises(self):
        with self.assertRaises(ValueError):
            self.account.deposit(0)

    def test_deposit_negative_raises(self):
        with self.assertRaises(ValueError):
            self.account.deposit(-10.0)

    def test_withdraw_reduces_balance(self):
        self.account.withdraw(40.0)
        self.assertEqual(self.account.get_balance(), 60.0)

    def test_withdraw_insufficient_funds_raises(self):
        with self.assertRaises(ValueError):
            self.account.withdraw(200.0)

    def test_withdraw_zero_raises(self):
        with self.assertRaises(ValueError):
            self.account.withdraw(0)

    def test_withdraw_negative_raises(self):
        with self.assertRaises(ValueError):
            self.account.withdraw(-5.0)

    def test_transaction_history_deposit(self):
        self.account.deposit(50.0)
        history = self.account.get_transaction_history()
        self.assertEqual(len(history), 1)
        self.assertIn("Einzahlung", history[0])

    def test_transaction_history_withdraw(self):
        self.account.withdraw(30.0)
        history = self.account.get_transaction_history()
        self.assertEqual(len(history), 1)
        self.assertIn("Abhebung", history[0])

    def test_transaction_history_multiple(self):
        self.account.deposit(50.0)
        self.account.withdraw(20.0)
        self.assertEqual(len(self.account.get_transaction_history()), 2)


if __name__ == "__main__":
    unittest.main()

class BankAccount:
    def __init__(self, owner, balance=0.0):
        if balance < 0:
            raise ValueError("Startguthaben kann nicht negativ sein")
        self.owner = owner
        self.balance = balance
        self.transactions = []

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Einzahlungsbetrag muss positiv sein")
        self.balance += amount
        self.transactions.append(f"Einzahlung: +{amount:.2f} EUR")

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Abhebebetrag muss positiv sein")
        if amount > self.balance:
            raise ValueError("Nicht genug Guthaben verfügbar")
        self.balance -= amount
        self.transactions.append(f"Abhebung: -{amount:.2f} EUR")

    def get_balance(self):
        return self.balance

    def get_transaction_history(self):
        return self.transactions

from bankaccount import BankAccount

all_accounts = []

john = BankAccount("John", "saving", 500)
all_accounts.append(john)

tim = BankAccount("Tim", "loan", -1000000)
all_accounts.append(tim)

sarah = BankAccount("Sarah", "saving", 0)
all_accounts.append(sarah)

john.deposit(3000)
print(f"John's current balance: {john.balance:,}\n")

print(f"Tim's loan balance: {tim.balance:,}")
payment = abs(tim.balance) / 2
tim.pay_loan(payment)
print(f"Tim paid {payment:,.2f}. New balance: {tim.balance:,}\n")

sarah.deposit(50000000)

sarah_loan = BankAccount("Sarah", "loan", -100000000)
all_accounts.append(sarah_loan)

print("Displaying all account information:")
for acc in all_accounts:
    acc.print_customer()
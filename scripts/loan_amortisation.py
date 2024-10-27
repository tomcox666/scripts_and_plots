import threading
from datetime import date, timedelta

class Loan:
    def __init__(self, loan_id, principal, interest_rate, term_years):
        self.loan_id = loan_id
        self.principal = principal
        self.interest_rate = interest_rate
        self.term_years = term_years
        self.monthly_payment = None  # Calculated later
        self.remaining_balance = principal

class Payment:
    def __init__(self, payment_id, date, amount, principal_portion, interest_portion, remaining_balance):
        self.payment_id = payment_id
        self.date = date
        self.amount = amount
        self.principal_portion = principal_portion
        self.interest_portion = interest_portion
        self.remaining_balance = remaining_balance

class LoanCalculator:
    def __init__(self):
        self.loans = {}
        self.lock = threading.Lock()  # To protect shared data

    def add_loan(self, loan):
        with self.lock:
            self.loans[loan.loan_id] = loan
            self.calculate_monthly_payment(loan)

    def calculate_monthly_payment(self, loan):
        monthly_rate = loan.interest_rate / 12 / 100
        num_payments = loan.term_years * 12
        loan.monthly_payment = (loan.principal * monthly_rate) / (1 - (1 + monthly_rate) ** -num_payments)

    def generate_amortization_schedule(self, loan_id):
        loan = self.loans[loan_id]
        schedule = []
        current_date = date.today()
        payment_id = 1

        while loan.remaining_balance > 0:
            interest_portion = loan.remaining_balance * (loan.interest_rate / 12 / 100)
            principal_portion = min(loan.monthly_payment - interest_portion, loan.remaining_balance)
            payment_amount = principal_portion + interest_portion

            loan.remaining_balance -= principal_portion

            payment = Payment(payment_id, current_date, payment_amount, principal_portion, interest_portion, loan.remaining_balance)
            schedule.append(payment)

            current_date += timedelta(days=30)  # Approximate month
            payment_id += 1

        return schedule

    def generate_schedules_concurrently(self, loan_ids):
        threads = []
        schedules = {}

        def worker(loan_id):
            schedule = self.generate_amortization_schedule(loan_id)
            with self.lock:
                schedules[loan_id] = schedule

        for loan_id in loan_ids:
            thread = threading.Thread(target=worker, args=(loan_id,))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()  # Wait for all threads to complete

        return schedules
        
# Create a calculator instance
calculator = LoanCalculator()

# Add the first loan
loan1 = Loan(loan_id="L123", principal=100000, interest_rate=5.0, term_years=30)
calculator.add_loan(loan1)

# Add a second loan
loan2 = Loan(loan_id="L456", principal=50000, interest_rate=4.0, term_years=15)
calculator.add_loan(loan2)

# Generate amortization schedules for both loans concurrently
loan_ids = ["L123", "L456"]
schedules = calculator.generate_schedules_concurrently(loan_ids)

# Print schedules for both loans
for loan_id, schedule in schedules.items():
    print(f"\nAmortization Schedule for Loan {loan_id}:")
    for payment in schedule:
        print(f"Payment ID: {payment.payment_id}, Date: {payment.date}, Amount: {payment.amount:.2f}, Principal: {payment.principal_portion:.2f}, Interest: {payment.interest_portion:.2f}, Balance: {payment.remaining_balance:.2f}")
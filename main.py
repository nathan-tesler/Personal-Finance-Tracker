import pandas as pd
import csv
from datetime import datetime
from data_entry import get_amount, get_category, get_date, get_description
import matplotlib.pyplot as plt

class CSV:
    CSV_FILE = "finance_data.csv"
    COLUMNS = ["date", "amount", "category", "description"]
    FORMAT= "%d-%m-%Y"

    @classmethod
    def intitialize_csv(cls):
        try:
            pd.read_csv(cls.CSV_FILE)
        except FileNotFoundError:
            df = pd.DataFrame(columns=cls.COLUMNS)
            df.to_csv(cls.CSV_FILE, index=False)

    @classmethod
    def add_entry(cls, date, amount, category, description):
        new_entry = {
            "date": date,
            "amount": amount,
            "category": category,
            "description": description
        }
        with open(cls.CSV_FILE, "a", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=cls.COLUMNS)
            writer.writerow(new_entry)
        print("Entry added successfully")

    @classmethod
    def remove_entry(cls, date, amount, category, description):
        df = pd.read_csv(cls.CSV_FILE)
        df['date'] = pd.to_datetime(df['date'], format=cls.FORMAT)

        entry_to_remove = (
            (df['date'] == pd.to_datetime(date, format=cls.FORMAT)) &
            (df['amount'] == amount) &
            (df['category'] == category) &
            (df['description'] == description)
        )
        if df[entry_to_remove].empty:
            print("No matching entry found to remove.")
        else:
            df = df[~entry_to_remove]
            df.to_csv(cls.CSV_FILE, index=False)
            print("Entry removed successfully.")

    @classmethod
    def get_transactions(cls, start_date, end_date):
        df = pd.read_csv(cls.CSV_FILE)
        df["date"] = pd.to_datetime(df["date"], format=CSV.FORMAT)
        start_date = datetime.strptime(start_date, CSV.FORMAT)
        end_date = datetime.strptime(end_date, CSV.FORMAT)
        
        mask = (df["date"] >= start_date) & (df["date"] <= end_date)
        filtered_df = df.loc[mask]

        if filtered_df.empty:
            print('No transaction found in the given date range')
        else:
            print(f"Transaction from {start_date.strftime(CSV.FORMAT)} to {end_date.strftime(CSV.FORMAT)}")
            print(filtered_df.to_string(index=False, formatters={"date": lambda x: x.strftime(CSV.FORMAT)}))

            total_income = filtered_df[filtered_df["category"] == "Income"]["amount"].sum()
            total_expense = filtered_df[filtered_df["category"] == "Expense"]["amount"].sum()
            print("\nSummary:")
            print(f"Total Income: ${total_income:.2f}")
            print(f"Total Expense: ${total_expense:.2f}")
            print(f"Net Savings: ${(total_income - total_expense):.2f}")

            return filtered_df

def add():
    CSV.intitialize_csv()
    date = get_date("Enter the date of the transaction (dd-mm-yyyy) or press enter for today's date: ", allow_default=True)
    amount = get_amount()
    category = get_category()
    description = get_description()
    CSV.add_entry(date, amount, category, description)

def remove():
    CSV.intitialize_csv()
    date = get_date("Enter the date of the transaction to remove (dd-mm-yyyy): ")
    amount = get_amount()
    category = get_category()
    description = get_description()
    CSV.remove_entry(date, amount, category, description)

def plot_transactions(df):
    df.set_index('date', inplace=True)
    income_df = df[df["category"] == "Income"].resameple("D").sum().reindex(df.index, fill_value=0)
    expense_df = df[df["category"] == "Expense"].resameple("D").sum().reindex(df.index, fill_value=0)
    plt.figure(figsize=(10, 5))
    plt.plot(income_df.index, income_df["amount"], label="Income", color="g")
    plt.plot(expense_df.index, expense_df["amount"], label="Expense", color='r')
    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.title("Income and Expenses")
    plt.legend()
    plt.grid(True)
    plt.show()

def main():
    while True:
        print("\n1. Add a new transaction")
        print("2. View transactions and summary within a date range")
        print("3. Remove a transaction")
        print("4. Exit")
        choice = input("Enter your choice(1-5): ")

        if choice == "1":
            add()
        elif choice == "2":
            start_date = get_date("Enter the start date (dd-mm-yyyy): ")
            end_date = get_date("Enter the end date (dd-mm-yyyy): ")
            df = CSV.get_transactions(start_date, end_date)
            if input("Do you want to see a plot? (y/n): ").lower() == "y":
                plot_transactions(df)
        elif choice == "3":
            remove()
        elif choice == "4":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Enter 1, 2, 3 or 4.")

if __name__ == "__main__":
    main()
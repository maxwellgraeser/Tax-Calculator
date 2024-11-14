import json
from datetime import datetime

DATA_FILE = "income_data.json"

# Function to calculate savings
def calculate_tax(income):
    return 0.3 * income

# Function to load income data from a file
def load_data():
    try:
        with open(DATA_FILE, 'r') as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = []
    return data

# Function to save income data to a file
def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

# Function to display income entries with indexes
def display_entries(data):
    if not data:
        print("No entries found.")
        return

    print("Income Entries:")
    for index, entry in enumerate(data):
        print(f"{index + 1}. Amount: ${entry['amount']:.2f}, Date: {entry['date']}")

# Function to calculate the total income and tax to set aside
def calculate_totals(data):
    total_income = sum(entry['amount'] for entry in data)
    total_tax = calculate_tax(total_income)
    return total_income, total_tax

# Main program
def main():
    # Load existing income data
    data = load_data()
    total_income, total_tax = calculate_totals(data)

    while True:
        print("\nOptions:")
        print("1. Add new income entry")
        print("2. View all entries")
        print("3. Remove an entry")
        print("4. View totals and tax to set aside")
        print("5. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            try:
                # Add a new income entry
                new_income = float(input("Enter new income amount: "))
                date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                data.append({"amount": new_income, "date": date_str})

                # Calculate tax for the new income entry only
                tax_for_new_entry = calculate_tax(new_income)
                
                # Update totals
                total_income, total_tax = calculate_totals(data)
                save_data(data)

                print(f"Income entry added. For this income of ${new_income:.2f}, set aside approximately ${tax_for_new_entry:.2f} for taxes.")
            except ValueError:
                print("Invalid input. Please enter a numeric value.")

        elif choice == "2":
            # View all entries
            display_entries(data)

        elif choice == "3":
            # Remove an entry
            display_entries(data)
            try:
                index = int(input("Enter the entry number to remove: ")) - 1
                if 0 <= index < len(data):
                    removed_entry = data.pop(index)
                    print(f"Removed entry: ${removed_entry['amount']:.2f} on {removed_entry['date']}")
                    
                    # Update totals and save data
                    total_income, total_tax = calculate_totals(data)
                    save_data(data)
                else:
                    print("Invalid entry number.")
            except ValueError:
                print("Please enter a valid number.")

        elif choice == "4":
            # View totals and tax to set aside
            print(f"\nTotal Income: ${total_income:.2f}")
            print(f"Total Tax to Set Aside: ${total_tax:.2f}")

        elif choice == "5":
            print("Exiting program.")
            break

        else:
            print("Invalid option. Please choose a number from 1 to 5.")

################################################################################################

# This is the original idea I had that calculated based on the graduated tax brackets.
# It isn't used in this program but I wanted to keep it for posterity sake.

# Constants for federal tax brackets for single filers 
TAX_BRACKETS = [
    (10275, 0.10),   # 10% on income up to $10,275
    (41775, 0.12),   # 12% on income over $10,275
    (89075, 0.22),   # 22% on income over $41,775
    (170050, 0.24),  # 24% on income over $89,075
    (215950, 0.32),  # 32% on income over $170,050
    (539900, 0.35),  # 35% on income over $215,950
    (float('inf'), 0.37)  # 37% on income over $539,900
]

def calculate_federal_tax(income):
    tax = 0
    remaining_income = income
    
    for limit, rate in TAX_BRACKETS:
        if remaining_income > limit:
            tax += limit * rate
            remaining_income -= limit
        else:
            tax += remaining_income * rate
            break
    
    return tax
################################################################################################

# Run the program
if __name__ == "__main__":
    main()
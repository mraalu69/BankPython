import random
import time
import requests

BASE_URL = 'http://localhost:5000'

def main_menu(is_existing_user):
    """Display the main menu based on user state."""
    if not is_existing_user:
        print("\n>>>>>>>>>>>>>>> Bank of Rahul <<<<<<<<<<<<<<<")
        print("1. Register a new user")
        print("2. Create a new account")
        print("3. Already a User")
        print("0. Exit")
    else:
        print("\nServices\n")
        print("4. Deposit money")
        print("5. Withdraw money")
        print("6. Check balance")
        print("9. Main menu")
        print("99. Profile")
        print("0. Exit")

def register_user():
    """Register a new user."""
    try:
        first_name = input("Enter Your First Name: ")
        last_name = input("Enter Your Last Name: ")
        phone_number = input("Enter Your Phone Number: ")

        response = requests.post(f'{BASE_URL}/register', json={
            'first_name': first_name,
            'last_name': last_name,
            'phone_number': phone_number
        })

        if response.status_code == 400:
            print(response.json().get('error'))
        else:
            print(f"User registered successfully with ID: {response.json()['user_id']}")
            print("You can now create a bank account.")

    except Exception as e:
        print(f"An error occurred during registration: {e}")

def create_account():
    """Create a new bank account for a registered user."""
    phone_number = input("Enter your registered phone number: ")
    
    response = requests.post(f'{BASE_URL}/create_account', json={'phone_number': phone_number})

    if response.status_code == 404:
        print(response.json().get('error'))
    elif response.status_code == 400:
        print(response.json().get('error'))
    else:
        account_data = response.json()
        print("Account created successfully")
        print(f"Name: {account_data['name']}")
        print(f"Phone: {account_data['phone_number']}")
        print(f"Account number: {account_data['account_number']}")
        print(f"Balance: {account_data['balance']}")

def deposit_money(account_number):
    """Deposit money into the current account."""
    amount = int(input("Enter amount to deposit: "))
    
    response = requests.post(f'{BASE_URL}/deposit', json={
        'account_number': account_number,
        'amount': amount
    })

    if response.status_code == 404:
        print(response.json().get('error'))
    else:
        print("Amount deposited successfully")
        print(f"New Balance: {response.json()['new_balance']}")

def withdraw_money(account_number):
    """Withdraw money from the current account."""
    amount = int(input("Enter amount to withdraw: "))
    
    response = requests.post(f'{BASE_URL}/withdraw', json={
        'account_number': account_number,
        'amount': amount
    })

    if response.status_code == 404:
        print(response.json().get('error'))
    elif response.status_code == 400:
        print(response.json().get('error'))
    else:
        print("Amount withdrawn successfully")
        print(f"New Balance: {response.json()['new_balance']}")

def check_balance(account_number):
    """Check the balance of the current account."""
    response = requests.get(f'{BASE_URL}/check_balance', params={'account_number': account_number})

    if response.status_code == 404:
        print(response.json().get('error'))
    else:
        print(f"Balance: {response.json()['balance']}")

def profile(account_number):
    """Display the profile of the current user."""
    response = requests.get(f'{BASE_URL}/profile', params={'account_number': account_number})

    if response.status_code == 404:
        print(response.json().get('error'))
    else:
        account = response.json()
        print("Hello, " + account['name'])
        print("\nPROFILE\n")
        print(f"Name: {account['name']}")
        print(f"Phone: {account['phone_number']}")
        print(f"Account number: {account['account_number']}")
        print(f"Balance: {account['balance']}")

def exit_program():
    """Exit the program after confirmation."""
    print("Are you sure?")
    back = input("1 for yes, 0 for no: ")
    if back == '1':
        print("Thank you for using our service.")
        exit()

def main_loop():
    is_existing_user = False
    current_account_number = None

    while True:
        try:
            main_menu(is_existing_user)
            choice = int(input("What service would you like to use: "))
            
            if not is_existing_user:
                if choice == 1:
                    register_user()
                elif choice == 2:
                    create_account()
                elif choice == 3:
                    phone_number = input("Enter your phone number: ")
                    response = requests.post(f'{BASE_URL}/create_account', json={'phone_number': phone_number})
                    if response.status_code == 200:
                        is_existing_user = True
                        current_account_number = response.json()['account_number']
                    else:
                        print(response.json().get('error'))
                elif choice == 0:
                    exit_program()
                else:
                    print("Invalid choice. Please try again.")
            else:
                if choice == 4:
                    deposit_money(current_account_number)
                elif choice == 5:
                    withdraw_money(current_account_number)
                elif choice == 6:
                    check_balance(current_account_number)
                elif choice == 9:
                    is_existing_user = False
                    current_account_number = None
                elif choice == 99:
                    profile(current_account_number)
                elif choice == 0:
                    exit_program()
                else:
                    print("Invalid choice. Please try again.")
        except ValueError:
            print("Please enter a valid number.")

if __name__ == "__main__":
    main_loop()

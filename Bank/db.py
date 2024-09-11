# db_operations.py
from pymongo import MongoClient

class DatabaseOperations:
    def __init__(self):
        """Initialize the database connection and collections."""
        self.client = MongoClient("mongodb+srv://yaronkarki12:r4hulk4rki@mydata.oxe0nxa.mongodb.net/")
        self.db = self.client.Bank
        self.accounts_collection = self.db.userData
        self.auth_collection = self.db.auth

    def user_exists(self, phone_number):
        """Check if a user with the given phone number exists."""
        return self.auth_collection.find_one({"phone_number": phone_number}) is not None

    def insert_user(self, first_name, last_name, phone_number):
        """Insert a new user into the auth collection."""
        user_data = {
            "first_name": first_name,
            "last_name": last_name,
            "phone_number": phone_number
        }
        result = self.auth_collection.insert_one(user_data)
        return result.inserted_id

    def get_user(self, phone_number):
        """Retrieve a user by phone number."""
        return self.auth_collection.find_one({"phone_number": phone_number})

    def account_exists(self, account_number):
        """Check if an account with the given account number exists."""
        return self.accounts_collection.find_one({"account_number": account_number}) is not None

    def insert_account(self, account_data):
        """Insert a new account into the accounts collection."""
        self.accounts_collection.insert_one(account_data)

    def get_account(self, account_number):
        """Retrieve an account by account number."""
        return self.accounts_collection.find_one({"account_number": account_number})

    def update_balance(self, account_number, new_balance):
        """Update the balance of an account."""
        self.accounts_collection.update_one(
            {"account_number": account_number},
            {"$set": {"balance": new_balance}}
        )
from flask import Flask, request, jsonify, render_template
from db import DatabaseOperations
import random
from bson.objectid import ObjectId

app = Flask(__name__)
db_ops = DatabaseOperations()

# Helper function to convert ObjectId to string in MongoDB documents
def convert_objectid(data):
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, ObjectId):
                data[key] = str(value)
    elif isinstance(data, list):
        data = [convert_objectid(item) for item in data]
    return data

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register_user():
    data = request.json
    first_name = data['first_name']
    last_name = data['last_name']
    phone_number = data['phone_number']
    
    if db_ops.user_exists(phone_number):
        return jsonify({"error": "User with this phone number already exists."}), 400
    
    user_id = db_ops.insert_user(first_name, last_name, phone_number)
    return jsonify({"user_id": str(user_id)})  # Convert ObjectId to string

@app.route('/create_account', methods=['POST'])
def create_account():
    data = request.json
    phone_number = data['phone_number']
    user = db_ops.get_user(phone_number)
    
    if not user:
        return jsonify({"error": "User not found. Please register first."}), 404
    
    account_number = random.randint(1111111111111111, 9999999999999999)
    
    if not db_ops.account_exists(account_number):
        account_data = {
            'account_number': account_number,
            'name': f"{user['first_name']} {user['last_name']}",
            'phone_number': phone_number,
            'balance': 0
        }
        db_ops.insert_account(account_data)
        account_data = convert_objectid(account_data)  # Ensure ObjectId is serialized
        return jsonify(account_data)
    else:
        return jsonify({"error": "Account already exists"}), 400

@app.route('/deposit', methods=['POST'])
def deposit_money():
    data = request.json
    account_number = data['account_number']
    amount = data['amount']
    
    if amount <= 0:
        return jsonify({"error": "Invalid amount"}), 400
    
    account = db_ops.get_account(account_number)
    if not account:
        return jsonify({"error": "Account not found"}), 404
    
    new_balance = account['balance'] + amount
    db_ops.update_balance(account_number, new_balance)
    return jsonify({"new_balance": new_balance})

@app.route('/withdraw', methods=['POST'])
def withdraw_money():
    data = request.json
    account_number = data['account_number']
    amount = data['amount']
    
    if amount <= 0:
        return jsonify({"error": "Invalid amount"}), 400
    
    account = db_ops.get_account(account_number)
    if not account:
        return jsonify({"error": "Account not found"}), 404
    
    if amount > account['balance']:
        return jsonify({"error": "Insufficient balance"}), 400
    
    new_balance = account['balance'] - amount
    db_ops.update_balance(account_number, new_balance)
    return jsonify({"new_balance": new_balance})

@app.route('/check_balance', methods=['GET'])
def check_balance():
    account_number = request.args.get('account_number')
    
    account = db_ops.get_account(account_number)
    if not account:
        return jsonify({"error": "Account not found"}), 404
    
    return jsonify({"balance": account['balance']})

@app.route('/profile', methods=['GET'])
def profile():
    account_number = request.args.get('account_number')
    
    account = db_ops.get_account(account_number)
    if not account:
        return jsonify({"error": "Account not found"}), 404
    
    account = convert_objectid(account)  # Ensure ObjectId is serialized
    return jsonify({
        "name": account['name'],
        "phone_number": account['phone_number'],
        "account_number": account['account_number'],
        "balance": account['balance']
    })

if __name__ == '__main__':
    app.run(debug=True)

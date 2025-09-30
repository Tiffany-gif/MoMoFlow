import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "..", "data", "processed", "sms_data.json")

def load_transactions():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_transactions(transactions):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(transactions, f, indent=4, ensure_ascii=False)

def get_transaction(tid):
    transactions = load_transactions()
    return next((tx for tx in transactions if str(tx["id"]) == str(tid)), None)

def add_transaction(data):
    transactions = load_transactions()
    new_id = max((tx["id"] for tx in transactions), default=0) + 1
    data["id"] = new_id
    transactions.append(data)
    save_transactions(transactions)
    return data

def update_transaction(tid, new_data):
    transactions = load_transactions()
    for tx in transactions:
        if str(tx["id"]) == str(tid):
            tx.update(new_data)
            save_transactions(transactions)
            return tx
    return None

def delete_transaction(tid):
    transactions = load_transactions()
    new_transactions = [tx for tx in transactions if str(tx["id"]) != str(tid)]
    if len(new_transactions) == len(transactions):
        return False
    save_transactions(new_transactions)
    return True


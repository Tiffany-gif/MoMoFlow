# MoMo SMS REST API — Documentation

**Base URL:** `http://localhost:8000`  
**Auth:** HTTP Basic Authentication

---

## Authentication

All endpoints require Basic Auth.

**Header example**
Authorization: Basic <base64("admin:password")>


**cURL helper**
```bash
# -u will add the Authorization header automatically
-u admin:password


Unauthenticated / wrong creds → 401 Unauthorized

{"error": "Unauthorized"}

Resource Model: Transaction

Your API stores transactions as raw JSON objects in data/processed/sms_data.json.
POST and PUT must include all fields (your team chose “keep it raw”).

Fields

{
  "protocol": "0",
  "address": "M-Money",
  "date": "1715807897054",
  "type": "1",
  "subject": "null",
  "body": "*113*R*A bank deposit of 5000 RWF has been added to your mobile money account at 2024-05-15 23:17:44. Your NEW BALANCE :5340 RWF. Cash Deposit::CASH::::0::250795963036.Thank you for using MTN MobileMoney.*EN#",
  "toa": "null",
  "sc_toa": "null",
  "service_center": "+250788110381",
  "read": "1",
  "status": "-1",
  "locked": "0",
  "date_sent": "1715807864000",
  "sub_id": "6",
  "readable_date": "15 May 2024 11:18:17 PM",
  "contact_name": "(Unknown)",
  "id": 30,
  "balance": 5340
}


id is assigned server-side on POST (auto-increment).
On PUT, id in the URL is the one that matters.

Endpoints
1) GET /transactions

Returns all transactions.

Request

curl -u admin:password http://localhost:8000/transactions


Response 200 OK

[
  {
    "protocol": "0",
    "address": "M-Money",
    "...": "...",
    "id": 30,
    "balance": 5340
  },
  { "...": "..." }
]

2) GET /transactions/{id}

Returns one transaction.

Request

curl -u admin:password http://localhost:8000/transactions/30


Response 200 OK

{
  "protocol": "0",
  "address": "M-Money",
  "...": "...",
  "id": 30,
  "balance": 5340
}


Not found 404 Not Found

{"error": "Transaction not found"}

3) POST /transactions

Creates a new transaction. Send ALL fields except id (server sets it).

Request

curl -u admin:password -X POST http://localhost:8000/transactions \
  -H "Content-Type: application/json" \
  -d '{
    "protocol": "0",
    "address": "M-Money",
    "date": "1715807897054",
    "type": "1",
    "subject": "null",
    "body": "Example SMS body text",
    "toa": "null",
    "sc_toa": "null",
    "service_center": "+250788110381",
    "read": "1",
    "status": "-1",
    "locked": "0",
    "date_sent": "1715807864000",
    "sub_id": "6",
    "readable_date": "15 May 2024 11:18:17 PM",
    "contact_name": "(Unknown)",
    "balance": 1234
  }'


Response 201 Created

{
  "...": "...",
  "id": 31
}


Bad request 400 Bad Request

{"error": "validation message"}

4) PUT /transactions/{id}

Updates an existing transaction by ID. Send ALL fields (raw mode).

Request

curl -u admin:password -X PUT http://localhost:8000/transactions/31 \
  -H "Content-Type: application/json" \
  -d '{
    "protocol": "0",
    "address": "M-Money",
    "date": "1715807897054",
    "type": "1",
    "subject": "null",
    "body": "Updated SMS body",
    "toa": "null",
    "sc_toa": "null",
    "service_center": "+250788110381",
    "read": "1",
    "status": "-1",
    "locked": "0",
    "date_sent": "1715807864000",
    "sub_id": "6",
    "readable_date": "15 May 2024 11:18:17 PM",
    "contact_name": "(Unknown)",
    "balance": 2000
  }'


Response 200 OK

{ "...": "...", "id": 31 }


Not found 404 Not Found

{"error": "Transaction not found"}


Bad request 400 Bad Request

{"error": "validation message"}

#5) DELETE /transactions/{id}

Deletes a transaction by ID.

Request

curl -u admin:password -X DELETE http://localhost:8000/transactions/31


Response 200 OK

{"message": "Transaction deleted"}


Not found 404 Not Found

{"error": "Transaction not found"}

Error Codes (Summary)

200 OK — Successful request.

201 Created — New transaction created.

400 Bad Request — Validation failed.

401 Unauthorized — Missing/invalid Basic Auth.

404 Not Found — Transaction ID not found.

Notes

Storage: JSON file at data/processed/sms_data.json

Validation: schemas.py (your server calls validate_transaction() on POST/PUT)

This API is intentionally framework-free (uses http.server) for learning.


---

# 2) `dsa_comparison.py`

```python
import os
import json
import time
import random

# --- Load the same JSON file your API uses ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "..", "data", "processed", "sms_data.json")

def load_transactions():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

# --- Linear search over list of dicts ---
def linear_search(transactions, target_id):
    for tx in transactions:
        if str(tx.get("id")) == str(target_id):
            return tx
    return None

# --- Build dict {id: tx} and lookup by key ---
def build_index(transactions):
    return { str(tx.get("id")): tx for tx in transactions }

def dict_lookup(index, target_id):
    return index.get(str(target_id))

def benchmark():
    transactions = load_transactions()
    n = len(transactions)
    print(f"[INFO] Loaded {n} transactions")

    if n == 0:
        print("No data to test.")
        return

    # prepare targets: mix of hits and misses
    ids_present = [tx["id"] for tx in transactions if "id" in tx]
    ids_present_str = [str(x) for x in ids_present]
    sample_size = min( max(20, n // 2), n)  # at least 20 if possible
    targets_hit = random.sample(ids_present_str, k=min(sample_size, len(ids_present_str)))
    targets_miss = [f"missing-{i}" for i in range(len(targets_hit))]  # guaranteed misses
    targets = targets_hit + targets_miss
    random.shuffle(targets)

    # repeat many times for stable timing
    iterations = 1000 if n >= 20 else 200

    # --- Linear search timing ---
    t0 = time.perf_counter()
    for _ in range(iterations):
        for tid in targets:
            linear_search(transactions, tid)
    t1 = time.perf_counter()
    linear_time = t1 - t0

    # --- Dict lookup timing ---
    index = build_index(transactions)
    t2 = time.perf_counter()
    for _ in range(iterations):
        for tid in targets:
            dict_lookup(index, tid)
    t3 = time.perf_counter()
    dict_time = t3 - t2

    speedup = linear_time / dict_time if dict_time > 0 else float("inf")

    print(f"[RESULT] Linear search time: {linear_time:.6f} s")
    print(f"[RESULT] Dict lookup time:  {dict_time:.6f} s")
    print(f"[RESULT] Speedup (linear/dict): {speedup:.2f}x")
    print("\nWhy dict is faster?")
    print("- Linear search checks elements one-by-one: O(n).")
    print("- Dictionary uses a hash table for near O(1) average-time lookups.")
    print("- As data grows, dict lookup scales much better for point queries.")

if __name__ == "__main__":
    benchmark()



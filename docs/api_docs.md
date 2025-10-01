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

5) DELETE /transactions/{id}

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



def validate_transaction(data: dict):
    required_fields = ["protocol", "address", "date", "type", "body"]

    for field in required_fields:
        if field not in data:
            return False, f"Missing required field: {field}"

    numeric_fields = ["balance", "fee"]
    for field in numeric_fields:
        if field in data and not isinstance(data[field], (int, float)):
            return False, f"{field} must be numeric"

    string_fields = ["transaction_id", "txid", "subject", "contact_name"]
    for field in string_fields:
        if field in data and not isinstance(data[field], str):
            return False, f"{field} must be a string"

    return True, None


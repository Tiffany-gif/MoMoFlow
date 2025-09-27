
import xml.etree.ElementTree as ET
import json
import os
import re

RAW_FILE = "data/raw/modified_sms_v2.xml"
PROCESSED_FILE = "data/processed/sms_data.json"


def parse_sms_xml():
    tree = ET.parse(RAW_FILE)
    root = tree.getroot()

    sms_list = []

    for i, sms in enumerate(root.findall(".//sms"), start=1):
        sms_data = {
            "protocol": sms.get("protocol"),
            "address": sms.get("address"),
            "date": sms.get("date"),
            "type": sms.get("type"),
            "subject": sms.get("subject"),
            "body": sms.get("body"),
            "toa": sms.get("toa"),
            "sc_toa": sms.get("sc_toa"),
            "service_center": sms.get("service_center"),
            "read": sms.get("read"),
            "status": sms.get("status"),
            "locked": sms.get("locked"),
            "date_sent": sms.get("date_sent"),
            "sub_id": sms.get("sub_id"),
            "readable_date": sms.get("readable_date"),
            "contact_name": sms.get("contact_name"),
            "id": i
        }

        body_text = sms_data["body"] or ""

        # Extract Financial Transaction Id
        match = re.search(r"Financial Transaction Id:\s*(\d+)", body_text)
        if match:
            sms_data["transaction_id"] = match.group(1)

        # Extract TxId
        match = re.search(r"TxId[:\s]+(\d+)", body_text)
        if match:
            sms_data["txid"] = match.group(1)

        # Extract Fee
        match = re.search(
            r"Fee (?:was|paid)[:\s]+(\d+)\s*RWF", body_text, re.IGNORECASE)
        if match:
            sms_data["fee"] = int(match.group(1))

        # Extract New Balance
        match = re.search(
            r"(?:Your new balance|NEW BALANCE)[:\s]+(\d+)\s*RWF", body_text, re.IGNORECASE)
        if match:
            sms_data["balance"] = int(match.group(1))

        sms_list.append(sms_data)

    os.makedirs(os.path.dirname(PROCESSED_FILE), exist_ok=True)

    with open(PROCESSED_FILE, "w", encoding="utf-8") as f:
        json.dump(sms_list, f, indent=4, ensure_ascii=False)

    return sms_list


if __name__ == "__main__":
    data = parse_sms_xml()
    print(f"Parsed {len(data)} SMS records. Saved to {PROCESSED_FILE}")

if data:
    print(f"\n Sample data (first SMS):")
    print(f"   ID: {data[0].get('id')}")
    print(f"   Date: {data[0].get('readable_date')}")
    print(f"   From: {data[0].get('address')}")
    print(f"   Body preview: {data[0].get('body', '')[:50]}...")

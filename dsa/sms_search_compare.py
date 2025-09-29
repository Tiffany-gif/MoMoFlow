import json
import os
import time
import random

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROCESSED_FILE = os.path.join(BASE_DIR, "data", "processed", "sms_data.json")


def load_sms():
    with open(PROCESSED_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def build_dict(sms_list):
    return {sms["id"]: sms for sms in sms_list}


def linear_search(sms_list, record_id):
    for sms in sms_list:
        if sms["id"] == record_id:
            return sms
    return None


def dict_lookup(sms_dict, record_id):
    return sms_dict.get(record_id, None)


def main():
    sms_list = load_sms()
    sms_dict = build_dict(sms_list)

    # Pick 20 random IDs from dataset
    test_ids = random.sample([sms["id"]
                             for sms in sms_list], min(20, len(sms_list)))

    linear_times, dict_times = [], []

    for rid in test_ids:
        start = time.perf_counter()
        linear_search(sms_list, rid)
        linear_times.append(time.perf_counter() - start)

        start = time.perf_counter()
        dict_lookup(sms_dict, rid)
        dict_times.append(time.perf_counter() - start)

    avg_linear = sum(linear_times) / len(linear_times)
    avg_dict = sum(dict_times) / len(dict_times)

    print("DSA Comparison: Linear Search vs Dictionary Lookup ")
    print(f"Average Linear Search Time (20 records): {avg_linear:.8f} seconds")
    print(
        f"Average Dictionary Lookup Time (20 records): {avg_dict:.8f} seconds")
    print(f"Dictionary lookup is ≈ {avg_linear/avg_dict:.1f}x faster\n")


if __name__ == "__main__":
    main()

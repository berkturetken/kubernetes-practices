from datetime import datetime
import random
import string
import os
import time
import urllib.request
import sys


IS_LOCAL = "--local" in sys.argv
if IS_LOCAL: # local
    OUTPUT_DIR = "./log_output/random_string_generator"
    PING_PONG_URL = "http://localhost:8080/pings"
else: # production
    OUTPUT_DIR = "/usr/src/app/files"
    PING_PONG_URL = "http://ping-pong-svc:4567/pings"

os.makedirs(OUTPUT_DIR, exist_ok=True)
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "output.log")


def get_pong_count():
    try:
        with urllib.request.urlopen(PING_PONG_URL, timeout=2) as response:
            return response.read().decode("utf-8").strip()
    except Exception as e:
        return "N/A"

def generate_random_string():
    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
    iso_timestamp = datetime.now().isoformat()
    pong_count = get_pong_count()
    return f"{iso_timestamp}: {random_string}\nPing / Pongs: {pong_count}"

while True:
    line = generate_random_string()
    with open(OUTPUT_FILE, "a") as f:
        f.write(line)
        f.write("\n")
    print(line.strip())
    time.sleep(5)
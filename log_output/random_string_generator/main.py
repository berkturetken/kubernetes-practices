from datetime import datetime
import random
import string
import os
import time

# For testing
# OUTPUT_DIR = "./log_output/random_string_generator"

# For production
OUTPUT_DIR = "/usr/src/app/files"
os.makedirs(OUTPUT_DIR, exist_ok=True)
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "output.log")


def generate_random_string():
    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
    iso_timestamp = datetime.now().isoformat()
    return f"{iso_timestamp}: {random_string}"

while True:
    line = generate_random_string()
    with open(OUTPUT_FILE, "a") as f:
        f.write(line)
        f.write("\n")
    print(line.strip())
    time.sleep(5)
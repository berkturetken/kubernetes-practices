from datetime import datetime
import random
import string
import time

random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=12))

while True:
    iso_timestamp = datetime.now().isoformat()
    print(f"{iso_timestamp}: {random_string}")
    time.sleep(5)
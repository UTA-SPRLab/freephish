import csv
import time
import requests
from requests.exceptions import RequestException

def check_url_status(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537',
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return 'active'
        else:
            return 'inactive'
    except RequestException:
        return 'inactive'

def update_csv(filename):
    with open(filename, mode='r') as file:
        reader = csv.reader(file)
        rows = [row for row in reader]

    for i in range(1, len(rows)):
        id, url, status = rows[i]
        if status != 'inactive':
            new_status = check_url_status(url)
            rows[i][2] = new_status

    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(rows)

if __name__ == "__main__":
    filename = 'urls.csv'
    while True:
        update_csv(filename)
        
        # Count how many URLs are still active
        with open(filename, mode='r') as file:
            reader = csv.reader(file)
            active_count = sum(1 for row in reader if row[2] == 'active')
        
        if active_count == 0:
            print("All URLs are inactive. Exiting.")
            break

        print("Sleeping for 10 minutes...")
        time.sleep(600)  # Sleep for 10 minutes


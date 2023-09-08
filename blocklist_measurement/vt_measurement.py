import csv
import os
import time
import requests

def is_active(url):
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return True
    except requests.RequestException:
        pass
    return False

def save_score(url_id, epoch_timestamp, response):
    os.makedirs("vt_scores/", exist_ok=True)
    with open(f"vt_scores/{url_id}_{epoch_timestamp}.txt", 'w') as file:
        file.write(str(response))

def run_virustotal(limit, filename):
    keylist = ['<Your_API_Key>', '<Another_API_Key>']
    key_index = 0

    counter_file = "vt_scores/vt_counter.txt"
    if not os.path.exists(counter_file):
        with open(counter_file, 'w') as f:
            f.write("0")

    with open(counter_file, 'r') as f:
        i = int(f.read())

    j = int(limit)

    while i < j:
        with open(filename, 'r') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)
            for row in csv_reader:
                if i >= j:
                    break
                
                url_id, url = row
                api_key = keylist[key_index]
                key_index = 1 - key_index

                if is_active(url):
                    params = {'apikey': api_key, 'url': url}
                    resp = requests.post('https://www.virustotal.com/vtapi/v2/url/scan', data=params)

                    time.sleep(600)  # Wait 10 minutes

                    params = {'apikey': api_key, 'resource': url}
                    resp = requests.get('https://www.virustotal.com/vtapi/v2/url/report', params=params)
                    response = resp.json()

                    epoch_timestamp = int(time.time())
                    save_score(url_id, epoch_timestamp, response)

                i += 1
                with open(counter_file, 'w') as f:
                    f.write(str(i))

                time.sleep(600)  # Wait 10 minutes


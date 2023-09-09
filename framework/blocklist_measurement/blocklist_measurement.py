import csv
import time
import requests
import os
import matplotlib.pyplot as plt

# Counters for each blocklist
phishtank_count = 0
ecx_count = 0
openphish_count = 0
gsb_count = 0

def download_ecx_file(temp_filename):
    os.system(f"""
    wget --quiet \
      --method GET \
      --header 'Authorization: <Enter eCX key here>' \
      --header 'Content-Type: application/json' \
      --output-document \
      - 'https://api.ecrimex.net/phish?container=csv' > {temp_filename}
    """)

def check_phishtank(url):
    global phishtank_count
    response = requests.get(f"https://checkurl.phishtank.com/checkurl/{url}")
    if response.json()['in_database']:
        phishtank_count += 1
        return True
    return False

def check_ecx(url, temp_filename):
    global ecx_count
    try:
        with open(temp_filename, 'r') as ecx_file:
            reader = csv.reader(ecx_file)
            for row in reader:
                if url in row:
                    ecx_count += 1
                    return True
    except Exception as e:
        print(f"Error in check_ecx: {e}")
    return False

def check_openphish(url):
    global openphish_count
    response = requests.get(f"https://openphish.com/feed.txt")
    if url in response.text:
        openphish_count += 1
        return True
    return False

def check_gsb(url):
    global gsb_count
    response = requests.post("https://safebrowsing.googleapis.com/v4/threatMatches:find",
        json={"client": {"clientId": "yourcompany", "clientVersion": "1.0"},
              "threatInfo": {"threatTypes": ["MALWARE", "SOCIAL_ENGINEERING"],
                             "platformTypes": ["ANY_PLATFORM"],
                             "threatEntryTypes": ["URL"],
                             "threatEntries": [{"url": url}]}})
    if response.json().get('matches'):
        gsb_count += 1
        return True
    return False

def plot_data():
    labels = ['PhishTank', 'ECX', 'OpenPhish', 'GSB']
    counts = [phishtank_count, ecx_count, openphish_count, gsb_count]
    plt.bar(labels, counts)
    plt.xlabel('Blocklist Service')
    plt.ylabel('Number of Detected URLs')
    plt.title('Number of URLs Detected by Each Blocklist')
    plt.show()

def check_urls(filename, temp_filename, loop=True, sleep_time=60):
    start_time = time.time()  # Initialize the start time for plotting
    ecx_download_time = 0  # Initialize the start time for eCrimex download

    while True:
        print("Checking URLs...")

        current_time = time.time()
        if current_time - ecx_download_time >= 10 * 60:  
            download_ecx_file(temp_filename)  # Download the eCrimex file
            ecx_download_time = current_time

        with open(filename, 'r') as file:
            reader = csv.reader(file)
            header = next(reader)
            for row in reader:
                url = row['url']  
                check_phishtank(url)
                check_ecx(url, temp_filename)
                check_openphish(url)
                check_gsb(url)

        if current_time - start_time >= 3 * 60 * 60:  
            print("Generating plot...")
            plot_data()
            start_time = current_time  # Update the start time for next interval

        if not loop:  
            break

        time.sleep(sleep_time)  # Sleep for a minute before the next iteration


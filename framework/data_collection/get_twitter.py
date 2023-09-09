import subprocess
import csv
import time
import os
from urllib.parse import urlparse
import requests

# Keywords
FWB_LIST = [
    'weebly', 'duckdns', '000webhost', 'blogspot', 'wix', 'sites.google', 'github.io',
    'firebase', 'square.site', 'forms.zoho', 'wordpress', 'docs.google', 'sharepoint',
    'yolasite', 'myftp.org', 'godaddy', 'mailchimp', 'atwebpages', 'glitch.me',
    'hpage', 'herokuapp', 'website.com', 'netlify'
]

# Resolve shortened URLs
def resolve_url(short_url):
    try:
        response = requests.get(short_url, timeout=10)
        return response.url
    except Exception as e:
        print(f"Error resolving URL {short_url}: {e}")
        return short_url  # return the original if it can't be resolved

# Function wrapping the main execution code
def get_twitter_posts():
    while True:
        with open('urls.csv', 'a', newline='') as master_csvfile:
            csvwriter = csv.writer(master_csvfile)
            if master_csvfile.tell() == 0:
                # Write header if the master file is empty
                csvwriter.writerow(['source', 'id', 'url', 'active', 'time_discovered'])

            for keyword in FWB_LIST:
                print(f"Getting posts for {keyword}...")
                
                # Generate filenames based on epoch time
                epoch_time = str(int(time.time()))
                jsonl_filename = f"raw/results_{epoch_time}_{keyword}.jsonl"
                csv_filename = f"raw/results_{epoch_time}_{keyword}.csv"

                # Execute twarc2 search command
                subprocess.run(["twarc2", "search", "--archive", f"url:{keyword}", jsonl_filename])

                # Convert JSONL to CSV using twarc2 csv
                subprocess.run(["twarc2", "csv", jsonl_filename, csv_filename])

                # Read the CSV file
                with open(csv_filename, 'r', newline='') as csvfile:
                    csvreader = csv.DictReader(csvfile)
                    for row in csvreader:
                        tweet_id = row['id']
                        link = row.get('expanded_url', '')
                        if link:
                            resolved_url = resolve_url(link)
                            parsed_url = urlparse(resolved_url)
                            if any(kw in parsed_url.netloc for kw in FWB_LIST):
                                # Write to master CSV
                                csvwriter.writerow([
                                    'twitter',
                                    tweet_id,
                                    resolved_url,  # Include the resolved URL
                                    'true',
                                    epoch_time
                                ])

        print("Sleeping for 10 minutes...")
        time.sleep(600)  # sleep for 10 minutes



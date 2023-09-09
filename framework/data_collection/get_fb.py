import csv
import time
import requests
from urllib.parse import urlparse

# CrowdTangle API endpoint and token
API_URL = "https://api.crowdtangle.com/posts"
API_TOKEN = "YOUR_CROWDTANGLE_API_TOKEN_HERE"

# Keywords
FWB_LIST = [
    'weebly', 'duckdns', '000webhost', 'blogspot', 'wix', 'sites.google', 'github.io',
    'firebase', 'square.site', 'forms.zoho', 'wordpress', 'docs.google', 'sharepoint',
    'yolasite', 'myftp.org', 'godaddy', 'mailchimp', 'atwebpages', 'glitch.me',
    'hpage', 'herokuapp', 'website.com', 'netlify'
]

def fetch_posts(api_url, token, query, count=100):
    params = {
        'token': token,
        'query': query,
        'count': count
    }
    response = requests.get(api_url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def get_fb_posts():
    while True:
        epoch_time = str(int(time.time()))
        csv_filename = f"raw/{epoch_time}.csv"
        
        with open(csv_filename, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            # Write header to include 'url'
            csvwriter.writerow(['source', 'id', 'url', 'active', 'time_discovered'])
                
            for keyword in FWB_LIST:
                print(f"Getting posts for {keyword}...")
                data = fetch_posts(API_URL, API_TOKEN, keyword)
                if data:
                    posts = data.get('result', {}).get('posts', [])
                    for post in posts:
                        post_id = post.get('id')
                        link = post.get('link')
                        
                        if link:
                            parsed_url = urlparse(link)
                            if any(kw in parsed_url.netloc for kw in FWB_LIST):
                                
                                csvwriter.writerow([
                                    'facebook',
                                    post_id,
                                    link,  # Include the URL
                                    'true',
                                    epoch_time
                                ])
                else:
                    print(f"Failed to retrieve data for keyword {keyword}")
        
        print("Sleeping for 10 minutes...")
        time.sleep(600)  

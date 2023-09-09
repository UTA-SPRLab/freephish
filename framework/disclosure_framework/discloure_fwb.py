import csv
import pandas as pd
from disclosure_framework.drivers.email_send import mail_send_module

# Function to check which domain the URL belongs to
def identify_provider(url, fwb_list):
    for domain in fwb_list:
        if domain in url:
            return domain
    return None

def find_abuse_email(keyword):
    df = pd.read_csv('registrar_info.csv')
    abuse_email = df[df['keyword'] == keyword]['abuse_email'].iloc[0]
    return abuse_email

def disclose_urls():
    # List of domains to check against
    fwb_list = ['weebly', 'duckdns', '000webhost', 'blogspot', 'wix', 'sites.google', 'github.io', 
                'firebase', 'square.site', 'forms.zoho', 'wordpress', 'docs.google', 'sharepoint', 
                'yolasite', 'myftp.org', 'godaddy', 'mailchimp', 'atwebpages', 'glitch.me', 
                'hpage', 'herokuapp', 'website.com', 'netlify']

    df_urls = pd.read_csv('parsed_metadata/features.csv')

    # Filter URLs where status is 'active' and reported_to_domain is 'false'
    filtered_urls = df_urls[(df_urls['status'] == 'active') & (df_urls['reported_to_domain'] == 'false')]

    for index, row in filtered_urls.iterrows():
        url = row['url']
        domain = identify_provider(url, fwb_list)

        if domain:
            abuse_email = find_abuse_email(domain)
            
            # Send the email
            mail_send_module(url, domain, abuse_email)
            
            df_urls.at[index, 'reported_to_domain'] = 'true'

    # Save the updated CSV back
    df_urls.to_csv('parsed_metadata/features.csv', index=False)



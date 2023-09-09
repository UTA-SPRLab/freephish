import csv
import re
import tldextract
import urllib
from difflib import SequenceMatcher
from nltk.corpus import stopwords
from collections import Counter
from urllib.parse import urlparse
import os
from pathlib import Path
import requests



def web_parser():

    # Load brands
    with open('brands.txt') as f:
        BRANDS = f.read().splitlines()

    # Load stopwords
    stop_words = set(stopwords.words('english'))

    # Load parsed IDs
    parsed_ids = []
    if os.path.exists('parsed_ids.txt'):
        with open('parsed_ids.txt') as f:
            parsed_ids = f.read().splitlines()

    feature_columns = [
        'ip_address', 'symbol_at', 'symbol_dash', 'symbol_tilde', 'https',
        'url_length', 'domain_length', 'dots_in_domain', 'sensitive_words',
        'tld_in_list', 'tld_in_domain', 'tld_in_path', 'internal_links',
        'external_links', 'empty_links', 'login_form', 'style_length',
        'script_length', 'link_length', '!--_length', 'form_length',
        'html_length', 'alarm_window', 'redirection', 'hidden_divs',
        'disabled_buttons', 'hidden_inputs', 'disabled_inputs', 'title_brand',
        'link_brand', 'top_brand_freq', 'link_internal', 'link_external',
        'img_internal', 'img_external', 'script_internal', 'script_external',
        'noscript_internal', 'noscript_external', 'brand_freq', 'html_embed',
        'brand_mimic'
    ]


    Path("parsed_metadata").mkdir(parents=True, exist_ok=True)  # create directory if doesn't exist
    with open('parsed_metadata/features.csv', 'w', newline='') as csvfile:
        fieldnames = ['id', 'url'] + feature_columns
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

    def load_html(url):
        # Load HTML content from URL
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.text
        except Exception as e:
            print(f"Error loading URL: {e}")
            return None

    def get_features(url, html):
        
        features = {}

        try:
            ip = urllib.parse.urlparse(url).netloc
            if re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', ip):
                features['ip_address'] = 1
            else:
                features['ip_address'] = 0
        except:
            features['ip_address'] = 0
            
        features['symbol_at'] = url.count('@')
        features['symbol_dash'] = url.count('-')
        features['symbol_tilde'] = url.count('~')
        
        features['https'] = 1 if url.startswith('https') else 0
        
        features['url_length'] = len(url)
        features['domain_length'] = len(tldextract.extract(url).domain)
        
        dots = tldextract.extract(url).domain.count('.')
        features['dots_in_domain'] = dots
        
        sens_words = ['secure', 'account', 'webscr', 'login', 
                      'ebayisapi', 'signin', 'banking', 'confirm']
        features['sensitive_words'] = sum([url.count(w) for w in sens_words])
        
        tld = tldextract.extract(url)
        features['tld_in_list'] = 1 if tld.suffix in tldextract.TLDS else 0
        features['tld_in_domain'] = tld.domain.count('.')
        features['tld_in_path'] = url.count('.') - features['tld_in_domain']
        
        # Similar target brand 
        max_ratio = 0
        for brand in BRANDS:
            ratio = SequenceMatcher(None, url, brand).ratio()
            if ratio > max_ratio:
                max_ratio = ratio

        links = re.findall(r'<a .*?>.*?</a>', html)
        domains = [urlparse(link).netloc for link in links]
        internal = len([d for d in domains if d == '' or d in html])
        external = len(domains) - internal
        features['internal_links'] = internal
        features['external_links'] = external
        
        # Empty links
        empty = re.findall(r'<a .*?>(\s|#)</a>', html)
        features['empty_links'] = len(empty)
        
        login_phrases = [
        'login', 'signin', 'log_in', 'sign_in', 'enter', 'access', 'auth', 
        'authentication', 'session', 'securelogin', 'securelog', 'userlogin', 
        'adminlogin', 'connect', 'join', 'authorize', 'authorise', 'account', 
        'startsession', 'logon', 'enteraccount', 'enterusr', 'usrlogin', 
        'credential', 'keyin', 'unlock', 'identification', 'idaccess', 'webaccess', 
        'useraccess', 'loginform', 'signinform', 'getin', 'logmein', 'loghere', 
        'accesshere', 'enterhere', 'username', 'userid', 'member', 'memberaccess', 
        'portal', 'webportal', 'siteaccess', 'siteentry', 'userentry', 'sitepass',
        'webpass', 'loginarea', 'clientlogin', 'customerlogin', 'guestlogin'
        ]

        pass_phrases = [
        'password', 'pass', 'passwd', 'passcode', 'pword', 'pwd', 
        'secret', 'secure', 'securitycode', 'pincode', 'pin', 'credential', 
        'key', 'accesskey', 'authkey', 'secretkey', 'code', 'passphrase', 
        'authenticate', 'verification', 'verify', 'token', 'safetycode', 
        'unlock', 'validation', 'validate', 'signcode', 'safekey', 
        'accesscode', 'privatekey', 'userpass', 'webpass', 'sitepass', 
        'enterpass', 'loginpass', 'app_pass', 'sitepassword', 'loginpassword', 
        'entrycode', 'confirmpass', 'authcode', 'passwd1', 'passwd2', 
        'memberpass', 'membercode', 'authorize', 'otp', 'onetimppass', 
        'dynamicpass', 'staticpass', 'mypass', 'secretcode', 'securecode'
        ]

        if re.search(rf'<form>.*?({"|".join(pass_phrases)}).*?({"|".join(login_phrases)})', html, flags=re.I):
            features['login_form'] = 1
        else:
            features['login_form'] = 0
            
        # HTML tag lengths 
        tags = ['style', 'script', 'link', '!--', 'form']
        for tag in tags:
            matches = re.findall(rf'<{tag}.*?>.*?</{tag}>', html)
            features[f'{tag}_length'] = sum(len(m) for m in matches) 
        features['html_length'] = len(html)
        
        # Alarm window
        features['alarm_window'] = 1 if 'alert(' in html else 0
        
        # Redirection
        features['redirection'] = 1 if 'redirect' in html else 0
        
        # Hidden elements
        features['hidden_divs'] = len(re.findall(r'<div .*?hidden.*?>', html))
        features['disabled_buttons'] = len(re.findall(r'<button .*?disabled.*?>', html)) 
        features['hidden_inputs'] = len(re.findall(r'<input .*?hidden.*?>', html))
        features['disabled_inputs'] = len(re.findall(r'<input .*?disabled.*?>', html))
        
        # Title vs URL brand
        title = re.search(r'<title>(.*?)</title>', html).groups()[0]
        url_brand = urlparse(url).netloc.split('.')[-2]
        features['title_brand'] = 1 if url_brand in title else 0
        
        # Frequent link brand vs URL brand
        links = re.findall(r'<a .*?>.*?</a>', html)
        brands = [link.split('/')[-1].split('.')[0] for link in links if '.' in link]
        brand_counts = Counter(brands)
        top_brand = brand_counts.most_common(1)[0][0]
        features['link_brand'] = 1 if url_brand == top_brand else 0
        features['top_brand_freq'] = brand_counts[top_brand]
        
        resources = ['link', 'img', 'script', 'noscript']
        for resource in resources:
            internal = len(re.findall(rf'<{resource} .*?>', html)) 
            external = len(re.findall(rf'<{resource} .*?//.*?>', html))
            features[f'{resource}_internal'] = internal
            features[f'{resource}_external'] = external
            
        # URL brand frequency
        features['brand_freq'] = html.lower().count(url_brand)
        
        # HTML string embedding 
        strings = re.findall(r'[^\s<>"]+|(?=<)|\n', html)
        filtered = [s for s in strings if s not in stop_words] 
        embed = [html_model[w] for w in filtered if w in html_model]
        features['html_embed'] = sum(embed) / len(embed)

        hidden_divs = len(re.findall(r'<div .*?hidden.*?>', html)) 
        return hidden_divs > 0
                
        features['brand_mimic'] = 1 if max_ratio > 0.8 else 0

        noindex = re.search(r'<meta.*?noindex.*?>', html)
        return 1 if noindex else 0


      return features


    # Process CSV files
    for filename in os.listdir('raw'):
        if filename.endswith('.csv'):
            with open(os.path.join('raw', filename)) as f:
                reader = csv.DictReader(f)
                
                for row in reader:
                    id = row['id']
                    url = row['url']
                    
                    if id not in parsed_ids:
                        html = load_html(url)
                        if html is not None:  # check if HTML was successfully fetched
                            features = get_features(url, html)
                            
                            # Append the new features to the existing CSV file
                            with open('parsed_metadata/features.csv', 'a', newline='') as csvfile:
                                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                                row_to_write = {'id': id, 'url': url}
                                row_to_write.update(features)
                                writer.writerow(row_to_write)
                            
                            # Record ID
                            parsed_ids.append(id)

    # Save parsed IDs
    with open('parsed_ids.txt', 'w') as f:
        f.write('\n'.join(parsed_ids))

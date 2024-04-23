from flask import Flask, request, jsonify
import re
import pandas as pd
from urllib.parse import urlparse
from tld import get_tld, is_tld
import joblib
import numpy as np

app = Flask(__name__)

# Load the saved model
loaded_model = joblib.load('RandomForest_19.pkl')

# Function to predict the class of a URL
def predict_url_class(url_features):
    # Make predictions using the loaded model
    prediction = loaded_model.predict(url_features)
    return prediction

# Domain feature extraction
def process_tld(url):
    try:
        res = get_tld(url, as_object=True, fail_silently=False, fix_protocol=True)
        pri_domain = res.parsed_url.netloc
    except:
        pri_domain = None
    return pri_domain

def digit_count(url):
    digits = 0
    for i in url:
        if i.isnumeric():
            digits += 1
    return digits

def letter_count(url):
    letters = 0
    for i in url:
        if i.isalpha():
            letters += 1
    return letters

def shortening_service(url):
    match = re.search(r'bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|'
                      r'yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|'
                      r'short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|'
                      r'doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|'
                      r'db\.tt|qr\.ae|adf\.ly|goo\.gl|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly|ity\.im|'
                      r'q\.gs|is\.gd|po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|'
                      r'x\.co|prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|'
                      r'tr\.im|link\.zip\.net',
                      url)
    if match:
        return 1
    else:
        return 0

def having_ip_address(url):
    match = re.search(
        r'(([01]?\d\d?|2[0-4]\d|25[0-5])\.([01]?\d\d?|2[0-4]\d|25[0-5])\.([01]?\d\d?|2[0-4]\d|25[0-5])\.'
        r'([01]?\d\d?|2[0-4]\d|25[0-5])\/)|'  # IPv4
        r'(([01]?\d\d?|2[0-4]\d|25[0-5])\.([01]?\d\d?|2[0-4]\d|25[0-5])\.([01]?\d\d?|2[0-4]\d|25[0-5])\.'
        r'([01]?\d\d?|2[0-4]\d|25[0-5])\/)|'  # IPv4 with port
        r'((0x[0-9a-fA-F]{1,2})\.(0x[0-9a-fA-F]{1,2})\.(0x[0-9a-fA-F]{1,2})\.(0x[0-9a-fA-F]{1,2})\/)'  # IPv4 in hexadecimal
        r'(?:[a-fA-F0-9]{1,4}:){7}[a-fA-F0-9]{1,4}|'
        r'([0-9]+(?:\.[0-9]+){3}:[0-9]+)|'
        r'((?:(?:\d|[01]?\d\d|2[0-4]\d|25[0-5])\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d|\d)(?:\/\d{1,2})?)', url)  # Ipv6
    if match:
        return 1
    else:
        return 0

def http_secure(url):
    htp = urlparse(url).scheme
    match = str(htp)
    if match == 'https':
        return 1
    else:
        return 0    

def abnormal_url(url):
    hostname = urlparse(url).hostname
    hostname = str(hostname)
    match = re.search(hostname, url)
    if match:
        return 1
    else:
        return 0

def extract_features(url):
    return pd.DataFrame({
        'url_len': [len(url)],
        '@': [url.count('@')],
        '?': [url.count('?')],
        '-': [url.count('-')],
        '=': [url.count('=')],
        '.': [url.count('.')],
        '#': [url.count('#')],
        '%': [url.count('%')],
        '+': [url.count('+')],
        '$': [url.count('$')],
        '!': [url.count('!')],
        '*': [url.count('*')],
        ',': [url.count(',')],
        '//': [url.count('//')],
        'abnormal_url': [abnormal_url(url)],
        'https': [http_secure(url)],  
        'digits': [digit_count(url)],
        'letters': [letter_count(url)],
        'Shortening_Service': [shortening_service(url)],
        'having_ip_address': [having_ip_address(url)],
    })

@app.route('/predict', methods=['POST'])
def predict():

    # Get the data sent by the client
    data = request.json

    # Extract features from the URL sent by the client
    url = str(data.get('url'))
    url = url.replace('www.', '')

    # Assuming the URL is sent in a JSON object with key 'url'
    # url_features = extract_features(url)

    # Predict the class of the URL using the extracted features
    prediction = predict_url_class(extract_features(url))
   # Convert prediction to a serializable data type
    prediction = int(prediction[0])  # Convert to integer

    # Return the prediction as JSON response
    return jsonify({
        'url': url,
        # 'prediction': prediction,
        'message': prediction,
    })

@app.route('/', methods=['GET'])
def index():
    return jsonify({'response': 'test'})

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, request, jsonify

app = Flask(__name__)

if __name__ == '__main__':
    app.run(debug=True)
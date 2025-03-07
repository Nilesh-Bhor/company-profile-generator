import json
import base64
import requests
from io import BytesIO

def get_logo(logo_url):
    try:
        response = requests.get(logo_url)
        if response.status_code == 200:
            return BytesIO(response.content)
    except:
        print(f"Error getting logo: {logo_url}")
    
    return None


def encode_profile_data(data):
    json_str = json.dumps(data)
    return base64.urlsafe_b64encode(json_str.encode()).decode()


def decode_profile_data(encoded_data):
    try:
        json_str = base64.urlsafe_b64decode(encoded_data.encode()).decode()
        return json.loads(json_str)
    except:
        return None
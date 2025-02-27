import requests
from io import BytesIO

def get_logo(logo_url):
    try:
        response = requests.get(logo_url)
        if response.status_code == 200:
            return BytesIO(response.content)
        return None
    except:
        return None
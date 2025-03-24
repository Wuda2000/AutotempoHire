import requestsimport osfrom dotenv import load_dotenv# Load environment variablesload_dotenv()CONSUMER_KEY = os.getenv("SAFARICOM_CONSUMER_KEY")CONSUMER_SECRET = os.getenv("SAFARICOM_CONSUMER_SECRET")# Consolidated get_access_token functiondef get_access_token():    """Generates OAuth access token for Safaricom API."""    url = "https://api.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"    response = requests.get(url, auth=(CONSUMER_KEY, CONSUMER_SECRET))        if response.status_code == 200:        return response.json().get("access_token")    else:        return None
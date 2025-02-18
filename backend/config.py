import requests

CLIENT_ID = "your-client-id"
CLIENT_SECRET = "your-client-secret"
TENANT_ID = "common"
REDIRECT_URI = "http://localhost:5000/callback"

def get_auth_url():
    return f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/authorize?client_id={CLIENT_ID}&response_type=code&redirect_uri={REDIRECT_URI}&scope=Mail.Send offline_access"

def get_token(auth_code):
    url = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token"
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": auth_code,
        "grant_type": "authorization_code",
        "redirect_uri": REDIRECT_URI
    }
    response = requests.post(url, data=data)
    return response.json().get("access_token")

def get_access_token():
    return get_token("your-auth-code")  # Replace with a valid auth code

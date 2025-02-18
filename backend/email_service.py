import requests
from config import CLIENT_ID, CLIENT_SECRET, TENANT_ID, get_access_token

def send_email(recipient, subject, body):
    token = get_access_token()
    url = "https://graph.microsoft.com/v1.0/me/sendMail"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    email_data = {
        "message": {
            "subject": subject,
            "body": {"contentType": "HTML", "content": body},
            "toRecipients": [{"emailAddress": {"address": recipient}}]
        }
    }

    response = requests.post(url, headers=headers, json=email_data)
    if response.status_code == 202:
        print("Email sent successfully!")
    else:
        print(f"Error: {response.text}")

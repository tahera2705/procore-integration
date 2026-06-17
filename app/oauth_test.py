import requests
import webbrowser

CLIENT_ID = os.getenv("PROCORE_CLIENT_ID")
CLIENT_SECRET = os.getenv("PROCORE_CLIENT_SECRET")

REDIRECT_URI = "http://localhost"
COMPANY_ID = "4285710"

# Step 1: Open OAuth authorization page
auth_url = (
    f"https://login-sandbox.procore.com/oauth/authorize"
    f"?response_type=code"
    f"&client_id={CLIENT_ID}"
    f"&redirect_uri={REDIRECT_URI}"
)
print("Opening browser for authorization...")
webbrowser.open(auth_url)

# Step 2: Paste authorization code
auth_code = input("Paste authorization code here: ").strip()

# Step 3: Exchange code for token
token_response = requests.post(
    "https://login-sandbox.procore.com/oauth/token",
    data={
        "grant_type": "authorization_code",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": auth_code,
        "redirect_uri": REDIRECT_URI,
    }
)

print("\nTOKEN RESPONSE:")
print(token_response.status_code)
print(token_response.text)

token_data = token_response.json()

if "access_token" not in token_data:
    print("\nToken exchange failed.")
    exit()

access_token = token_data["access_token"]

response = requests.get(
    "https://api.procore.com/rest/v1.0/me",
    headers={
        "Authorization": f"Bearer {access_token}"
    }
)

print("\nAPI RESPONSE:")
print(response.status_code)
print(response.text)
# Step 4: Call Procore API
response = requests.get(
    "https://api.procore.com/rest/v1.0/me",
    headers={
        "Authorization": f"Bearer {access_token}"
    }
)

print("\nAPI RESPONSE:")
print(response.status_code)
print(response.text)
print("\nAPI RESPONSE:")
print(response.status_code)
print(response.text)
print(token_data["scope"])
print(access_token[:50])
print(len(access_token))
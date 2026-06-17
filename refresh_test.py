import requests

CLIENT_ID = "GeVyY_eRjJ1dAbSTl8D3CGRcxh9tUMwETOjRmuUJe60"
CLIENT_SECRET = "mlwRhJSJQdxaBm7ZkQucwjWjEgJBiTzcFUVRwUKMCoo"

REFRESH_TOKEN = "HUeC6JUSCkakmykIGb2qvrn0UsUMC08XjIwoDAEyG7w"

response = requests.post(
    "https://login-sandbox.procore.com/oauth/token",
    data={
        "grant_type": "refresh_token",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "refresh_token": REFRESH_TOKEN
    }
)

print("STATUS:")
print(response.status_code)

print("\nRESPONSE:")
print(response.text)
token_data = response.json()

access_token = token_data["access_token"]

headers = {
    "Authorization": f"Bearer {access_token}"
}

api_response = requests.get(
    "https://api.procore.com/rest/v1.0/me",
    headers=headers
)

print("\nAPI STATUS:")
print(api_response.status_code)

print("\nAPI RESPONSE:")
print(api_response.text)
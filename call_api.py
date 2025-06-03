import requests
import json
import os
import time

AUTH0_DOMAIN = "dev-k5tma83wlfoi88qe.us.auth0.com"
CLIENT_ID = "BjwM81mdYLcJwCZGQKUSQ44DY3Ex0NYr"
CLIENT_SECRET = "Zc_0ZbJKOcq-VyLSX9G6ijPQW0WyLYp6OdAkED5j7eHYdN_9f5bXxwMhWLLbQly8"
AUDIENCE = "https://api.example.com"
API_URL = "https://zk8xx60iqd.execute-api.us-east-1.amazonaws.com/prod/hello"
TOKEN_FILE = "token.json"

#Testing purpose

def get_saved_token():
    if not os.path.exists(TOKEN_FILE):
        return None
    with open(TOKEN_FILE, "r") as f:
        data = json.load(f)
    # Check if token is still valid (with 60s buffer)
    if data["expires_at"] > time.time() + 60:
        return data["access_token"]
    return None

def fetch_new_token():
    token_url = f"https://{AUTH0_DOMAIN}/oauth/token"
    token_data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "audience": AUDIENCE,
        "grant_type": "client_credentials"
    }
    resp = requests.post(token_url, json=token_data)
    resp.raise_for_status()
    token_json = resp.json()
    access_token = token_json["access_token"]
    expires_in = token_json.get("expires_in", 3600)
    expires_at = int(time.time()) + expires_in
    # Save token and expiry
    with open(TOKEN_FILE, "w") as f:
        json.dump({"access_token": access_token, "expires_at": expires_at}, f)
    return access_token

def get_token():
    token = get_saved_token()
    if token:
        print("Using cached token.")
        return token
    print("Fetching new token.")
    return fetch_new_token()

def main():
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.get(API_URL, headers=headers)
    print("API response:", resp.status_code, resp.text)
    with open("output.txt", "w") as f:
        f.write(resp.text)

if __name__ == "__main__":
    main()
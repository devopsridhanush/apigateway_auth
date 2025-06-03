import requests

AUTH0_DOMAIN = "dev-k5tma83wlfoi88qe.us.auth0.com"
CLIENT_ID = "BjwM81mdYLcJwCZGQKUSQ44DY3Ex0NYr"
CLIENT_SECRET = "Zc_0ZbJKOcq-VyLSX9G6ijPQW0WyLYp6OdAkED5j7eHYdN_9f5bXxwMhWLLbQly8"
AUDIENCE = "https://api.example.com"
API_URL = "https://zk8xx60iqd.execute-api.us-east-1.amazonaws.com/prod/hello"

# Get token
token_url = f"https://{AUTH0_DOMAIN}/oauth/token"
token_data = {
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
    "audience": AUDIENCE,
    "grant_type": "client_credentials"
}
token_resp = requests.post(token_url, json=token_data)
token_resp.raise_for_status()
token = token_resp.json()["access_token"]
print("TOKEN:", token)

# Call API
headers = {"Authorization": f"Bearer {token}"}
api_resp = requests.get(API_URL, headers=headers)
print("API response:", api_resp.status_code, api_resp.text)

# Optionally, write output to a file for artifact
with open("output.txt", "w") as f:
    f.write(api_resp.text)
import json
import jwt
import urllib.request
from jwt import PyJWKClient

AUTH0_DOMAIN = 'dev-k5tma83wlfoi88qe.us.auth0.com'
API_AUDIENCE = 'https://api.example.com'
ALGORITHMS = ['RS256']

def lambda_handler(event, context):
    print("Event received:", json.dumps(event))
    token = ''

    # Support both standard and TOKEN authorizer events
    if 'authorizationToken' in event:
        auth_header = event['authorizationToken']
        print("authorizationToken:", auth_header)
        if auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
    else:
        headers = event.get('headers', {})
        auth_header = headers.get('Authorization') or headers.get('authorization', '')
        print("Headers:", headers)
        print("Authorization header:", auth_header)
        if auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]

    print("Token:", token)

    if not token:
        print("No token found.")
        raise Exception("Unauthorized")

    try:
        jwks_url = f'https://{AUTH0_DOMAIN}/.well-known/jwks.json'
        print("JWKS URL:", jwks_url)
        jwk_client = PyJWKClient(jwks_url)
        signing_key = jwk_client.get_signing_key_from_jwt(token)
        print("Signing Key:", signing_key.key)

        payload = jwt.decode(
            token,
            signing_key.key,
            algorithms=ALGORITHMS,
            audience=API_AUDIENCE,
            issuer=f'https://{AUTH0_DOMAIN}/'
        )
        print("Payload:", payload)

        return generate_policy(payload['sub'], 'Allow', event['methodArn'])

    except Exception as e:
        print("Authorization error:", str(e))
        raise Exception("Unauthorized")

def generate_policy(principal_id, effect, resource):
    return {
        'principalId': principal_id,
        'policyDocument': {
            'Version': '2012-10-17',
            'Statement': [{
                'Action': 'execute-api:Invoke',
                'Effect': effect,
                'Resource': resource
            }]
        }
    }

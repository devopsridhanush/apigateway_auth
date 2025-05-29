# Auth0 + API Gateway + Lambda Authorizer PoC (Python Version)

This project uses Python Lambda functions to secure an AWS API Gateway endpoint using a JWT token from Auth0.

## Files

- `authorizer/lambda_function.py`: JWT verification Lambda authorizer using Auth0
- `backend/lambda_function.py`: Protected backend Lambda

## Setup

1. Replace `YOUR_AUTH0_DOMAIN` in the authorizer with your actual Auth0 domain.
2. Deploy the Lambda functions using AWS Console or SAM.
3. Create a REST API Gateway:
   - Attach the Lambda Authorizer to a method
   - Protect your backend Lambda
4. Call the API with a valid JWT in the `Authorization` header.


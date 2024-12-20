# MyInfo API Integration with Django REST Framework

This Django project integrates with the Singapore government’s MyInfo API to allow users to authenticate, retrieve access tokens, and fetch their personal data. The application exposes API endpoints to facilitate the OAuth2 flow and retrieve encrypted personal data.

## Features

- **Authorization URL Generation**: Generate the URL for users to authenticate via MyInfo.
- **Access Token Retrieval**: Fetch access tokens using authorization codes.
- **Retrieve Personal Data**: Fetch and decrypt user data using access tokens.

## API Endpoints

### 1. **Generate Authorization URL**
   - **URL**: `/myinfo/auth-url/`
   - **Method**: `GET`
   - **Description**: Generates the MyInfo authorization URL to initiate the authentication flow.
   - **Response**:
     ```json
     {
       "auth_url": "https://myinfo.gov.sg/authorize?client_id=...&scope=...&...&code_challenge=...",
       "code_verifier": "randomly_generated_code_verifier"
     }
     ```

### 2. **Retrieve Access Token**
   - **URL**: `/myinfo/access-token/`
   - **Method**: `POST`
   - **Description**: Retrieves the access token from MyInfo API using the authorization code.
   - **Payload**:
     ```json
     {
       "auth_code": "your-auth-code",
       "oauth_state": "your-oauth-state",
       "code_verifier": "your-code-verifier"
     }
     ```
   - **Response**:
     ```json
     {
       "access_token": "your-access-token"
     }
     ```

### 3. **Retrieve User Data**
   - **URL**: `/myinfo/retrieve-data/`
   - **Method**: `POST`
   - **Description**: Retrieves user data from MyInfo API using the access token.
   - **Payload**:
     ```json
     {
       "access_token": "your-access-token"
     }
     ```
   - **Response** (example):
     ```json
     {
       "uinfin": "S1234567A",
       "name": "John Doe",
       "dob": "1980-01-01",
       "email": "john.doe@example.com",
       ...
     }
     ```

## Requirements

- Python 3.x
- Django 3.x or 4.x
- Django REST Framework
- Requests

### Install Dependencies
```bash
pip install -r requirements.txt

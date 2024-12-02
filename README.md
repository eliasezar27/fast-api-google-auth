# Staizen App
## Overview
This project provides a FastAPI-based OAuth2 authentication service that integrates with Google OAuth for login and registration. It securely manages user authentication and stores user data in a SQLite database. This also includes file upaload and streaming with valid user token (bearer).

## Features:
- Google OAuth2 Authentication
- JWT Token Generation and Validation
- File upload and streaming

## Pre-requisites
1. Python 3.8 or latest
2. [Setup GCP OAuth and Credentials](#setup-google-cloud-oauth-and-credentials) (Downloading the key file in here is important)

## Installation
1. Clone the repository:
    ```bash
   git clone https://github.com/eliasezar27/fast-api-google-auth.git
   ```
2. Navigate to the project directory:
    ```bash
   cd fast-api-google-auth
   ```
3. Create your own `.env` file, use the `env.template` for reference.
    e.g.
    ```
    SECRET_KEY=1234567890
    ALGORITHM=HS256
    DOMAIN=http://127.0.0.1:8080
    GOOGLE_CLIENT_SECRET_FILE_PATH=secret.json
    ACCESS_TOKEN_EXPIRE_MINUTES=240
    ```
4. Copy and paste Oauth client file retrieved from `Google Cloud Platform > API & Services > Credentials` inside the `staizen_app` directory.
5. Create your Python environment, ensure that your active path in the terminal is the root directory
    ```bash
    python -m venv venv # for winOS
    python3 -m venv venv # for macOS
    ```
6. Install dependencies:
    ```bash
   pip install -r requirements.txt
   ```
7. For running locally just execute the following:
   ```bash
   cd staizen_app
   uvicorn app:app --host 127.0.0.1 --port 8080
   ```

## Run in Docker (Local or in Server)
1. Clone the repository:
    ```bash
   git clone https://github.com/eliasezar27/fast-api-google-auth.git
   ```
2. Navigate to the project directory:
    ```bash
   cd fast-api-google-auth
   ```
3. Create your own `.env` file, use the `env.template` for reference.
    e.g.
    ```
    SECRET_KEY=1234567890
    ALGORITHM=HS256
    DOMAIN=http://127.0.0.1:8080
    GOOGLE_CLIENT_SECRET_FILE_PATH=secret.json
    ACCESS_TOKEN_EXPIRE_MINUTES=240
    ```
4. Copy and paste Oauth client file retrieved from `Google Cloud Platform > API & Services > Credentials` inside the `staizen_app` directory.
5. Run docker compose command. Ensure that you are back in the root directory.
    ```bash
   docker-compose up --build -d
   ```


## Running Routes
1. **/google/auth/login**
    - Open a browser, paste this route e.g. http://localhost:8080/google/auth/login
    - Follow the login steps with your preferred account.
    - Once done copy the access token from the `access_token` field to be used as token in the streaming route.

2. **/stream/stream_file**
    - Open postman and paste the cUrl command below:
    ```bash
    curl --location 'http://localhost:8080/stream/stream_file' \
    --header 'accept: application/json' \
    --header 'authorization: Bearer <token>' \
    --form 'file=@"/<path_to_file>"'
    ```
    - Hit send

---
# Setup Google Cloud Oauth and Credentials
1. **Visit the Google Cloud Console**:
   - Open [Google Cloud Console](https://console.cloud.google.com/).
2. **Sign In**:
   - Log in using your Google account.
3. **Create a New Project**:
   - Click the project dropdown in the top navigation bar.
   - Click **New Project**.
   - Provide a **Project Name**, optionally set an organization, and click **Create**.
4. **Wait for Project Creation**:
   - Once the project is created, select it from the project dropdown.

#### Step 2: Enable APIs for the Project
1. **Navigate to API & Services**:
   - Go to **APIs & Services** from the left-hand menu.
   - Select **Library**.
2. **Enable the Required APIs**:
   - Search for **People API**
   - Click the API, then click **Enable**.

#### Step 3: Create OAuth 2.0 Client ID
1. **Go to Credentials**:
   - Navigate to **APIs & Services > Credentials**.
2. **Set Up the OAuth Consent Screen**:
   - Click **OAuth Consent Screen** in the left menu.
   - Select **External**.
   - Fill in the required fields (App name, User supported email, Developer contact information).
   - Click **Save and Continue**. 
   - For scopes, click ADD OR REMOVE SCOPES.
   - Add `auth/userinfo` in the filter text box and tick all results and click **update**.
   - Click **Save and Continue**. 
   - On the test users page, add your own email address.
   - Click **Save and Continue**.
3. **Create Credentials**:
   - Go back to **APIs & Services > Credentials**.
   - Click **Create Credentials** and select **OAuth Client ID**.
4. **Configure OAuth 2.0 Client ID**:
   - Choose **Application Type** Web Application.
   - Add in the domain in the **Authorized JavaScript origins** in this case is `http://127.0.0.1:8080`.
   - Provide the **Redirect URIs** in this case is `http://127.0.0.1:8080/google/auth/oauth2callback`.
   - Click **Create**.

#### Step 4: Download the Client File
1. **Download the Credentials**:
   - After creating the OAuth 2.0 Client ID, you’ll see it listed under the **OAuth 2.0 Client IDs** section.
   - Click the **Download Icon** (shaped like a downward arrow) in the Actions column next to your Client ID.
2. **Save the File**:
   - Save the downloaded JSON file securely. This file contains sensitive credentials.

#### Step 5: Include JSON file in the Application main directory
1. **Store the File**:
   - Place the JSON file inside the `staizen_app` directory.
2. **Set Environment Variable**:
   - In the `.env` file change the **GOOGLE_CLIENT_SECRET_FILE_PATH** value to the JSON file's filename.

#### Notes:
- Avoid sharing the downloaded client file publicly.
- Use the JSON file only in secure environments.
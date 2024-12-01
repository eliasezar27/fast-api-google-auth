# Staizen App
## Overview
This project provides a FastAPI-based OAuth2 authentication service that integrates with Google OAuth for login and registration. It securely manages user authentication and stores user data in a SQLite database. This also includes file upaload and streaming with valid user token (bearer).

## Features:
- Google OAuth2 Authentication
- JWT Token Generation and Validation
- File upload and streaming


## Installation
1. Clone the repository:
    ```bash
   git clone https://github.com/eliasezar27/fast-api-google-auth.git
   ```
2. Navigate to the project directory:
    ```
   cd fast-api-google-auth
   ```
3. Create your own `.env` file, use the `env.template` for reference.
4. Create your Python environment
    ```bash
    python -m venv venv # for winOS
    python3 -m venv venv # for macOS
    ```
5. Install dependencies:
    ```bash
   pip install -r requirements.txt
   ```


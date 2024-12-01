from fastapi import  Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from core.models.database import Session, get_db
from core.constants.constant import ALGORITHM, SECRET_KEY
from core.dao.UserDAO import UserDAO


# OAuth2 Dependency
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="google/auth/login")

# Helper function to encode a JWT
def encode_jwt(user_info):
    return jwt.encode(user_info, SECRET_KEY, algorithm=ALGORITHM)


# Helper function to decdoe a JWT
def decode_jwt(user_info):
    return jwt.decode(user_info, SECRET_KEY, algorithm=[ALGORITHM])


# Helper function to mask user_id
def mask_user_id(user_id: int) -> str:
    return jwt.encode({"user_id": user_id}, SECRET_KEY, algorithm=ALGORITHM)


# Helper function to unmask user_id
def unmask_user_id(masked_id: str) -> int:
    try:
        payload = decode_jwt(masked_id, SECRET_KEY, algorithms=[ALGORITHM])
        return payload["user_id"]
    except JWTError:
        raise HTTPException(status_code=400, detail="Invalid masked user ID")

# Function to decode and validate the token
def verify_token(token: str, db: Session = Depends(get_db)):
    try:
        payload = decode_jwt(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")

        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: user_id not found",
                headers={"WWW-Authenticate": "Bearer"},
            )
        # Optionally, verify user exists in the database
        user_dao = UserDAO(db)
        user = user_dao.get_user_by_id(user_id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: user not found",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user  # Return user data if valid
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )

# Dependency to get the current user
def verify_current_user(token: str = Depends(oauth2_scheme)):
    return verify_token(token)
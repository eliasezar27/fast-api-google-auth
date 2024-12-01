from fastapi import  Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from typing import Optional
import datetime

# Import from internal modules
from core.models.database import Session, get_db
from core.constants.constant import ALGORITHM, SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES
from core.dao.UserDAO import UserDAO


# OAuth2 Dependency
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="google/auth/login")

# Helper function to encode a JWT
def encode_jwt(user_info, secret_key = SECRET_KEY, algorithm = ALGORITHM):
    return jwt.encode(user_info, secret_key, algorithm=algorithm)


# Helper function to decdoe a JWT
def decode_jwt(user_info, secret_key = SECRET_KEY, algorithms = [ALGORITHM]):
    return jwt.decode(user_info, secret_key, algorithms=algorithms)


# Helper function to mask user_id
def mask_user_id(user_id: int) -> str:
    return encode_jwt({"user_id": user_id})


# Helper function to unmask user_id
def unmask_user_id(masked_id: str) -> int:
    try:
        payload = decode_jwt(masked_id, SECRET_KEY, algorithms=[ALGORITHM])
        return payload["user_id"]
    except JWTError:
        raise HTTPException(status_code=400, detail="Invalid masked user ID")


# Function to decode the token and validate the user ID
def verify_user_id(token: str, db: Session):
    try:
        token = str(token)
        payload = decode_jwt(token)
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
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )


# Dependency to get the current user
def verify_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    return verify_user_id(token, db)


def create_access_token(data: dict, expires_delta: Optional[datetime.timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.datetime.now(datetime.timezone.utc) + expires_delta
    else:
        expire = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = encode_jwt(to_encode)
    return encoded_jwt
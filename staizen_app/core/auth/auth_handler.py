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

def encode_jwt(info, secret_key = SECRET_KEY, algorithm = ALGORITHM):
    '''
    Helper function that encodes using jwt
    '''
    return jwt.encode(info, secret_key, algorithm=algorithm)


def decode_jwt(info, secret_key = SECRET_KEY, algorithms = [ALGORITHM]):
    '''
    Helper function that decodes using jwt
    '''
    return jwt.decode(info, secret_key, algorithms=algorithms)


def mask_user_id(user_id: int) -> str:
    '''
    Helper function that masks user ID
    '''
    return encode_jwt({"user_id": user_id})


def unmask_user_id(masked_id: str) -> int:
    '''
    Helper function that unmasks user ID
    '''
    try:
        payload = decode_jwt(masked_id,)
        return payload["user_id"]
    except JWTError:
        raise HTTPException(status_code=400, detail="Invalid masked user ID")


def verify_user(token: str, db: Session):
    '''
    Function to decode the token and validate the user ID.
    '''
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


def verify_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    '''
    Dependency function for verifying and validating token.
    '''
    return verify_user(token, db)


def create_access_token(data: dict, expires_delta: Optional[datetime.timedelta] = None):
    '''
    Function that creates time limited token
    '''
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.datetime.now(datetime.timezone.utc) + expires_delta
    else:
        expire = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = encode_jwt(to_encode)
    return encoded_jwt
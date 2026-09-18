from datetime import datetime, timedelta, timezone

import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from pwdlib import PasswordHash
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


router = APIRouter()

SECRET_KEY = "your_secret_key"
algorithm = "HS256"
TOKEN_EXPIRATION_MINUTES = 15

password_hasher = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

USER = {
    "username": "alice",
    "password": password_hasher.hash("secret"),
}


def create_token(username: str) -> str:
    payload = {
        "sub": username,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=TOKEN_EXPIRATION_MINUTES),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=algorithm)


def current_user(token: str = Depends(oauth2_scheme)) -> str:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[algorithm])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return username
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

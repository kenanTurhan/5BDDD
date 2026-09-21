from datetime import datetime, timedelta, timezone

import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from pwdlib import PasswordHash
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import dotenv
import os

dotenv.load_dotenv()

router = APIRouter()

SECRET_KEY = os.getenv("SECRET_KEY")
algorithm = "HS256"
TOKEN_EXPIRATION_MINUTES = 15

bearer_scheme = HTTPBearer()



def create_token(username: str) -> str:
    payload = {
        "sub": username,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=TOKEN_EXPIRATION_MINUTES),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=algorithm)


def current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[algorithm])
        return payload["sub"]
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expiré")
    except (jwt.InvalidTokenError, KeyError):
        raise HTTPException(status_code=401, detail="Token invalide")
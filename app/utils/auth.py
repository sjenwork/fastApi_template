from fastapi import HTTPException
from fastapi import Depends
from app.utils.security_utils import generate_hashed_key
from fastapi.security.api_key import APIKeyHeader
import os

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)
api_user_header = APIKeyHeader(name="AccId", auto_error=False)


def get_user(AccId: str = Depends(api_user_header)):
    if AccId is None:
        raise HTTPException(status_code=403, detail="Could not validate credentials")
    return {"AccId": AccId}


def get_api_key(api_key: str = Depends(api_key_header)):
    key = os.getenv("API_KEY")
    salt = os.getenv("API_SALT")
    expected_api_key = generate_hashed_key(key, salt)
    if api_key != expected_api_key:
        raise HTTPException(status_code=403, detail="Could not validate credentials")
    return api_key

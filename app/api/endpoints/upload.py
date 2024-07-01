from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi import FastAPI, Body, Depends, HTTPException, status, File, UploadFile, Request
from fastapi.security import OAuth2PasswordBearer
from starlette.responses import JSONResponse
from fastapi.security.api_key import APIKeyHeader
import os


# ----- ref: 生成 API 密鑰方式 -----
import secrets
import hashlib
import os


# 生成 API 密鑰
def generate_api_key(length=32):
    return secrets.token_hex(length)


# 生成 salt
def generate_salt(length=16):
    return secrets.token_hex(length)


# 使用 API 密鑰和 salt 生成哈希值
def generate_hashed_key(api_key, salt):
    return hashlib.sha256(f"{api_key}{salt}".encode()).hexdigest()


def run_generate_api_key():
    key = generate_api_key()
    salt = input("Enter salt: ")
    hashed_key = generate_hashed_key(key, salt)
    print(f"API Key: `{key}`")
    print(f"hashed Key: `{hashed_key}`")


# ----- ref: 生成 API 密鑰方式 -----


router = APIRouter()

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


def get_api_key(api_key: str = Depends(api_key_header)):
    api_key = os.getenv("API_KEY")
    salt = os.getenv("API_SALT")
    expected_api_key = generate_hashed_key(api_key, salt)
    if api_key != expected_api_key:
        raise HTTPException(status_code=403, detail="Could not validate credentials")
    return api_key


@router.post("/upload/", dependencies=[Depends(get_api_key)])
async def upload_file(file: UploadFile = File(...)):
    """
    上傳檔案的路由處理程序。

    Args:
        file (UploadFile): 上傳的檔案。

    Returns:
        JSONResponse: 上傳結果的回應。
    """
    print(file.filename)
    try:
        with open(f"uploaded_{file.filename}", "wb") as buffer:
            buffer.write(file.file.read())
        return {"filename": file.filename, "message": "File uploaded successfully!"}
    except Exception as e:
        return JSONResponse(content={"message": f"Error: {e}"}, status_code=400)


@router.get("/test/", dependencies=[Depends(get_api_key)])
async def test():
    return {"message": "Hello, World in Upload!"}

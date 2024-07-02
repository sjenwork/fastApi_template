from fastapi import APIRouter, Depends, HTTPException
from fastapi import Depends, HTTPException, File, UploadFile, Request
from starlette.responses import JSONResponse
from fastapi.security.api_key import APIKeyHeader

from app.utils.logger.create_logger import loggerWrapper
from app.utils.security_utils import generate_hashed_key
import os


router = APIRouter()

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


def get_api_key(api_key: str = Depends(api_key_header)):
    key = os.getenv("API_KEY")
    salt = os.getenv("API_SALT")
    expected_api_key = generate_hashed_key(key, salt)
    if api_key != expected_api_key:
        raise HTTPException(status_code=403, detail="Could not validate credentials")
    return api_key


@router.post("/upload/", dependencies=[Depends(get_api_key)])
@loggerWrapper
async def upload_file(AccId: str, file: UploadFile = File(...)):
    """
    上傳檔案的路由處理程序。

    Args:
        file (UploadFile): 上傳的檔案。

    Returns:
        JSONResponse: 上傳結果的回應。
    """
    print(file.filename)
    try:
        with open(f"/Api/upload_data/{file.filename}", "wb") as buffer:
            buffer.write(file.file.read())
        return {"filename": file.filename, "message": "File uploaded successfully!"}
    except Exception as e:
        return JSONResponse(content={"message": f"Error: {e}"}, status_code=400)


@router.get("/test/")
@loggerWrapper
async def test(AccId: str):
    return {"message": "Hello, World in Upload!"}

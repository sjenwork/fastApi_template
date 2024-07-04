from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Request
from starlette.responses import JSONResponse
from app.utils.auth import get_api_key, get_user


router = APIRouter()


@router.post("/upload/", dependencies=[Depends(get_api_key)])
@router.post("/upload", dependencies=[Depends(get_api_key)])
# @loggerWrapper
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


@router.get("/test", dependencies=[Depends(get_user)])
# @loggerWrapper
async def test(AccId: str):
    return {"message": "Hello, World in Upload!"}

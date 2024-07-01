import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


import requests
import os
from app.api.endpoints.upload import generate_hashed_key


def upload_file(fn):
    url = os.getenv("API_URL")
    key = os.getenv("API_KEY")
    if not url:
        url = input("請輸入 URL: ")
    if not key:
        key = input("請輸入 key: ")
    salt = input("Enter salt: ")
    api_key = generate_hashed_key(key, salt)
    headers = {"X-API-Key": api_key}
    with open(fn, "rb") as file:
        response = requests.post(
            url,
            files={
                "file": file,
            },
            headers=headers,
        )
        print(response.json())


upload_file(fn="/Users/jen/work/demo/test/data/testfile.txt")

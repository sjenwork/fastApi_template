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


def generate_sha512_hash(input_string: str) -> str:
    sha512 = hashlib.sha512()
    sha512.update(input_string.encode("utf-8"))
    return sha512.hexdigest()

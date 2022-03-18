import base64

from fastapi import HTTPException, status

def decode_photo(path, encode_str: str) -> None:
    with open(path, "wb") as f:
        try:
            f.write(base64.b64decode(encode_str.encode('utf-8')))
        except Exception as ex:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid photo encoding")
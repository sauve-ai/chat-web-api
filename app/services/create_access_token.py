from jose import JWTError, jwt

from app.services import setting

def create_access_token(data: dict, expires_delta: None):
    to_encode = data.copy()
    to_encode.update({"exp": expires_delta})
    encoded_jwt = jwt.encode(
                                to_encode,
                                setting.SECRET_KEY,
                                algorithm=setting.ALGORITHM
                            )
    return encoded_jwt
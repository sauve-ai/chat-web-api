from jose import JWTError, jwt

from datetime import datetime, timedelta, timezone

from app.services import setting

def create_access_token(data: dict, expires_delta: None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
                                to_encode,
                                setting.SECRET_KEY,
                                algorithm=setting.ALGORITHM
                            )
    return encoded_jwt
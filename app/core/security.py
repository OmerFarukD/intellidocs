from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import JWTError, jwt
import hashlib
import base64
from app.core.config import settings

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
def _prepare_password(password: str) -> str:
    """
    Uzun şifreleri bcrypt'e güvenli vermek için SHA-256'ya al.
    Bu sayede 72 karakter sınırı aşılmaz.
    """
    hashed = hashlib.sha256(password.encode()).digest()
    return base64.b64encode(hashed).decode()

def hash_password(password: str) -> str:
    return pwd_context.hash(_prepare_password(password))

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(_prepare_password(plain), hashed)
def create_access_token(data:dict)->str:
    to_encode = data.copy()
    expire = datetime.now() + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({'exp':expire})
    return jwt.encode(to_encode,settings.SECRET_KEY,algorithm=settings.ALGORITHM)

def decode_token(token: str) -> dict:
    return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])


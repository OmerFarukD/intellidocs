from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, Select
from app.models.user import User
from app.core.security import hash_password, verify_password, create_access_token

async  def register(email:str, password:str, db:AsyncSession)->User:
    result = await db.execute(select(User).where(User.email == email))
    if result.scalar_one_or_none():
        raise ValueError('Bu email zaten kayıtlı.')
    user = User(
        email = email,
        hashed_password= hash_password(password)
    )
    db.add(user)
    await db.flush()
    return user


async def login(email:str, password:str, db:AsyncSession) ->str:
    result = await db.execute(Select(User).where(User.email==email))
    user = result.scalar_one_or_none()

    if not user or not verify_password(password, user.hashed_password):
        raise ValueError('Email veya şifre hatalı.')

    return create_access_token({'sub':str(user.id), 'email':user.email})
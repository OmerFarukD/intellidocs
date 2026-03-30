from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.user import UserRegister, UserLogin, TokenResponse, UserResponse
from app.services import auth_service

router = APIRouter(prefix='/auth', tags=['auth'])
@router.post('/register', response_model=UserResponse)
async def register(data:UserRegister,db:AsyncSession = Depends(get_db)):
    try:
        user = await auth_service.register(data.email, data.password,db)
        return user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login", response_model=TokenResponse)
async def login(data: UserLogin, db: AsyncSession = Depends(get_db)):
    try:
        token = await auth_service.login(data.email,data.password,db)
        return {'access_token':token}
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))


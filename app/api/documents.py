from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.user import User
from app.services import document_service
router = APIRouter(prefix="/documents", tags=["documents"])

@router.post("/upload")
async def upload_document(
        file: UploadFile = File(...),
        db:AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):

    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail='Sadece PDF yüklenebilir')

    file_bytes = await file.read()

    if len(file_bytes) > 10 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="Dosya 10 MB dan büyük olamaz.")
    doc = await document_service.upload_document(
        user_id=current_user.id,
        filename=file.filename,
        file_bytes=file_bytes,
        db=db
    )
    return {
        "id": doc.id,
        "filename": doc.filename,
        "collection_id": doc.chroma_collection_id
    }
@router.get("/list")
async def list_documents(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    docs = await document_service.get_user_documents(current_user.id, db)
    return [{"id": d.id, "filename": d.filename} for d in docs]

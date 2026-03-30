# app/services/document_service.py
import uuid
import tempfile
import os
import chromadb

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

from app.models.document import Document
from app.core.config import settings


async def upload_document(
    user_id: int,
    filename: str,
    file_bytes: bytes,
    db: AsyncSession
) -> Document:

    # 1. Geçici dosyaya kaydet
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(file_bytes)
        tmp_path = tmp.name

    try:
        # 2. PDF yükle ve chunk'lara böl
        loader = PyPDFLoader(tmp_path)
        pages = loader.load()

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50
        )
        chunks = splitter.split_documents(pages)

        # 3. Collection ID oluştur
        collection_id = f"user_{user_id}_{uuid.uuid4().hex[:8]}"

        # 4. ChromaDB'ye indexle
        embeddings = OpenAIEmbeddings(
            model="text-embedding-3-small",
            api_key=settings.OPENAI_API_KEY
        )

        chroma_client = chromadb.HttpClient(
            host=settings.CHROMA_HOST,
            port=settings.CHROMA_PORT
        )

        chroma_client.get_or_create_collection(collection_id)

        Chroma(
            client=chroma_client,
            collection_name=collection_id,
            embedding_function=embeddings,
        ).add_documents(chunks)

        # 5. PostgreSQL'e metadata kaydet
        document = Document(
            user_id=user_id,
            filename=filename,
            chroma_collection_id=collection_id
        )
        db.add(document)
        await db.flush()

        return document

    finally:
        # 6. Geçici dosyayı sil
        os.unlink(tmp_path)


async def get_user_documents(user_id: int, db: AsyncSession) -> list[Document]:
    result = await db.execute(
        select(Document).where(Document.user_id == user_id)
    )
    return result.scalars().all()
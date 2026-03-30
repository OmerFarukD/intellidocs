import chromadb
from app.core.config import settings

def get_chroma_client():
    return chromadb.HttpClient(
        host=settings.CHROMA_HOST,
        port=settings.CHROMA_PORT
    )

def get_or_create_collection(user_id:int, document_id: int):
    client = get_chroma_client()
    collection_name = f"user_{user_id}_doc_{document_id}"
    return client.get_or_create_collection(name=collection_name)


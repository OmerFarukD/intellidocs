
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

`requirements.txt`:
```
fastapi
uvicorn
sqlalchemy
alembic
asyncpg
psycopg2-binary
pydantic-settings
python-jose
passlib[bcrypt]
python-multipart
langchain
langchain-openai
langchain-community
chromadb
pypdf
python-dotenv
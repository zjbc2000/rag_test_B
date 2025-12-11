from pathlib import Path

from app.config import Settings
from app.services.embedder import SentenceTransformerEmbedder
from app.services.log_repo import SearchLogRepo
from app.services.vector_store import ChromaVectorStore

settings = Settings()

# 预创建目录，避免首次访问失败
Path(settings.chroma_dir).mkdir(parents=True, exist_ok=True)
Path(settings.log_db_path).parent.mkdir(parents=True, exist_ok=True)

embedder = SentenceTransformerEmbedder(settings.embedding_model)
vector_store = ChromaVectorStore(settings.chroma_dir)
log_repo = SearchLogRepo(settings.log_db_path)


def get_settings() -> Settings:
    return settings


def get_embedder() -> SentenceTransformerEmbedder:
    return embedder


def get_vector_store() -> ChromaVectorStore:
    return vector_store


def get_log_repo() -> SearchLogRepo:
    return log_repo


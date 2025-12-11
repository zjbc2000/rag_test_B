from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    chroma_dir: str = "data/chroma"
    log_db_path: str = "data/search_logs.db"
    chunk_size: int = 300
    chunk_overlap: int = 50
    default_top_k: int = 4

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


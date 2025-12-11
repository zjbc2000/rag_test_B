from dataclasses import dataclass
from typing import Any, Dict, List
from uuid import uuid4

import chromadb


@dataclass
class DocumentChunk:
    id: str
    text: str
    metadata: Dict[str, Any]


class ChromaVectorStore:
    def __init__(self, persist_dir: str) -> None:
        self.client = chromadb.PersistentClient(path=persist_dir)
        self.collection = self.client.get_or_create_collection(
            "documents", metadata={"hnsw:space": "cosine"}
        )

    def upsert(self, chunks: List[DocumentChunk], embeddings: List[List[float]]) -> None:
        if not chunks:
            return
        self.collection.upsert(
            ids=[chunk.id for chunk in chunks],
            documents=[chunk.text for chunk in chunks],
            metadatas=[chunk.metadata for chunk in chunks],
            embeddings=embeddings,
        )

    def query(self, embedding: List[float], top_k: int) -> List[DocumentChunk]:
        res = self.collection.query(
            query_embeddings=[embedding],
            n_results=top_k,
            include=["documents", "metadatas", "distances"],
        )
        documents = res.get("documents", [[]])[0]
        metadatas = res.get("metadatas", [[]])[0]
        distances = res.get("distances", [[]])[0]
        ids = res.get("ids", [[]])[0]

        results: List[DocumentChunk] = []
        for doc_id, doc, meta, dist in zip(ids, documents, metadatas, distances):
            meta = meta or {}
            meta.update({"score": dist})
            results.append(DocumentChunk(id=doc_id, text=doc, metadata=meta))
        return results


def new_chunk_id() -> str:
    return uuid4().hex


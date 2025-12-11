from time import perf_counter
from typing import List

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Request

from app import schemas
from app.dependencies import (
    get_embedder,
    get_log_repo,
    get_settings,
    get_vector_store,
)
from app.services.chunker import chunk_text
from app.services.vector_store import DocumentChunk, new_chunk_id

router = APIRouter()


@router.post("/ingest", response_model=dict)
async def ingest(
    payload: schemas.IngestRequest,
    settings=Depends(get_settings),
    embedder=Depends(get_embedder),
    vector_store=Depends(get_vector_store),
) -> dict:
    chunk_size = payload.chunk_size or settings.chunk_size
    chunk_overlap = payload.chunk_overlap or settings.chunk_overlap
    chunks = chunk_text(payload.text, chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    if not chunks:
        raise HTTPException(status_code=400, detail="文本为空，无法切块")

    doc_chunks: List[DocumentChunk] = []
    for idx, text in enumerate(chunks):
        doc_chunks.append(
            DocumentChunk(
                id=new_chunk_id(),
                text=text,
                metadata={"source": payload.source or "user", "chunk_index": idx},
            )
        )

    embeddings = embedder.embed([c.text for c in doc_chunks])
    vector_store.upsert(doc_chunks, embeddings)
    return {"chunks": len(doc_chunks)}


@router.post("/search", response_model=schemas.SearchResponse)
async def search(
    payload: schemas.SearchRequest,
    request: Request,
    background_tasks: BackgroundTasks,
    settings=Depends(get_settings),
    embedder=Depends(get_embedder),
    vector_store=Depends(get_vector_store),
    log_repo=Depends(get_log_repo),
) -> schemas.SearchResponse:
    top_k = payload.top_k or settings.default_top_k
    if top_k <= 0:
        raise HTTPException(status_code=400, detail="top_k 必须大于 0")

    start = perf_counter()
    query_vec = embedder.embed([payload.query])[0]
    results = vector_store.query(query_vec, top_k)
    latency_ms = (perf_counter() - start) * 1000

    response_results = [
        schemas.SearchResult(
            id=item.id,
            text=item.text,
            score=item.metadata.get("score", 0.0),
            metadata={k: v for k, v in item.metadata.items() if k != "score"},
        )
        for item in results
    ]

    # 异步记录日志
    background_tasks.add_task(
        log_repo.write_log,
        query_text=payload.query,
        top_k=top_k,
        latency_ms=latency_ms,
        requester_ip=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent"),
        results=[
            {
                "id": r.id,
                "score": r.metadata.get("score", 0.0),
                "metadata": r.metadata,
            }
            for r in results
        ],
    )

    return schemas.SearchResponse(count=len(response_results), results=response_results)


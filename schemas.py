from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class IngestRequest(BaseModel):
    text: str = Field(..., description="需要切块并入库的文本")
    source: Optional[str] = Field(None, description="文本来源标识")
    chunk_size: Optional[int] = Field(None, description="覆盖默认 chunk 大小")
    chunk_overlap: Optional[int] = Field(None, description="覆盖默认 chunk 重叠长度")


class SearchRequest(BaseModel):
    query: str = Field(..., description="检索文本")
    top_k: Optional[int] = Field(None, description="返回数量")


class SearchResult(BaseModel):
    id: str
    text: str
    score: float
    metadata: Dict[str, Any]


class SearchResponse(BaseModel):
    count: int
    results: List[SearchResult]


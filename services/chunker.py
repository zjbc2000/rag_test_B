from typing import List


def chunk_text(text: str, chunk_size: int = 300, chunk_overlap: int = 50) -> List[str]:
    """
    简单的按字符长度滑动窗口切块。
    """
    cleaned = text.strip()
    if not cleaned:
        return []

    chunks: List[str] = []
    start = 0
    length = len(cleaned)
    effective_size = max(chunk_size, 1)
    overlap = max(min(chunk_overlap, effective_size - 1), 0)

    while start < length:
        end = min(start + effective_size, length)
        chunks.append(cleaned[start:end])
        if end == length:
            break
        start = end - overlap

    return chunks


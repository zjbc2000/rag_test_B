from typing import List

from sentence_transformers import SentenceTransformer


class SentenceTransformerEmbedder:
    """
    简单封装 sentence-transformers，便于替换实现。
    """

    def __init__(self, model_name: str) -> None:
        self.model_name = model_name
        self._model: SentenceTransformer | None = None

    def _get_model(self) -> SentenceTransformer:
        if self._model is None:
            self._model = SentenceTransformer(self.model_name)
        return self._model

    def warmup(self) -> None:
        """
        预热模型以减少首个请求延迟。
        """
        self.embed(["warmup"])

    def embed(self, texts: List[str]) -> List[List[float]]:
        model = self._get_model()
        embeddings = model.encode(texts, normalize_embeddings=True)
        return embeddings.tolist()


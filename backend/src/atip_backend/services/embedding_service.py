from sentence_transformers import SentenceTransformer


class EmbeddingService:
    """Generate vector embeddings for document text."""

    MODEL_NAME = "BAAI/bge-m3"

    def __init__(self) -> None:
        self.model = SentenceTransformer(
            self.MODEL_NAME,
        )

    def embed_text(
        self,
        text: str,
    ) -> list[float]:
        """Generate a normalized embedding for text."""

        embedding = self.model.encode(
            text,
            normalize_embeddings=True,
        )

        return embedding.tolist()

    def embed_texts(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        """Generate normalized embeddings for multiple texts."""

        embeddings = self.model.encode(
            texts,
            normalize_embeddings=True,
            show_progress_bar=False,
        )

        return embeddings.tolist()

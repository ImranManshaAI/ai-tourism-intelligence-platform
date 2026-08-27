class DocumentChunker:
    """Split extracted document pages into overlapping text chunks."""

    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 150,
    ) -> None:
        if chunk_size <= 0:
            raise ValueError(
                "chunk_size must be greater than zero"
            )

        if chunk_overlap < 0:
            raise ValueError(
                "chunk_overlap cannot be negative"
            )

        if chunk_overlap >= chunk_size:
            raise ValueError(
                "chunk_overlap must be smaller than chunk_size"
            )

        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def chunk_pages(
        self,
        pages: list[dict],
    ) -> list[dict]:
        """Split extracted pages into chunks while preserving page numbers."""

        chunks: list[dict] = []
        chunk_index = 0

        for page in pages:
            page_number = page["page_number"]
            text = page["text"].strip()

            if not text:
                continue

            start = 0
            text_length = len(text)

            while start < text_length:
                end = min(
                    start + self.chunk_size,
                    text_length,
                )

                chunk_text = text[start:end].strip()

                if chunk_text:
                    chunks.append(
                        {
                            "chunk_index": chunk_index,
                            "content": chunk_text,
                            "page_number": page_number,
                        }
                    )

                    chunk_index += 1

                if end >= text_length:
                    break

                start = end - self.chunk_overlap

        return chunks

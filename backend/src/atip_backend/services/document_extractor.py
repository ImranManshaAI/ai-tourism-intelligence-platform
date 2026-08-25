from pathlib import Path

from pypdf import PdfReader


class DocumentExtractor:
    """Extract text from supported document formats."""

    def extract_pdf(self, file_path: str | Path) -> list[dict]:
        """Extract text from a PDF while preserving page numbers."""

        reader = PdfReader(str(file_path))

        pages: list[dict] = []

        for page_number, page in enumerate(reader.pages, start=1):
            text = page.extract_text() or ""

            pages.append(
                {
                    "page_number": page_number,
                    "text": text,
                }
            )

        return pages

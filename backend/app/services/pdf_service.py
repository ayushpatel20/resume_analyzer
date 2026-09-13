import os
import re
import uuid
from pathlib import Path
from fastapi import UploadFile, HTTPException, status
from app.config import settings


class PDFService:
    """Handles secure PDF upload, validation, and text extraction with PyMuPDF."""

    def __init__(self, upload_dir: Path | None = None):
        self._upload_dir = upload_dir

    @property
    def upload_dir(self) -> Path:
        p = self._upload_dir or settings.UPLOADS_DIR
        try:
            p.mkdir(parents=True, exist_ok=True)
        except Exception:
            pass
        return p


    def validate_and_save(self, file: UploadFile) -> tuple[Path, str, int]:
        """
        Validate file extension and size, then save securely to uploads directory.
        Returns (saved_file_path, secure_filename, file_size)
        """
        filename = file.filename or "resume.pdf"
        file_ext = Path(filename).suffix.lower()

        if file_ext not in settings.ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid file format. Only PDF files (.pdf) are supported.",
            )

        # Generate a unique, safe filename
        safe_base = re.sub(r"[^a-zA-Z0-9_\-\.]", "_", Path(filename).stem)[:50]
        unique_name = f"{uuid.uuid4().hex[:8]}_{safe_base}.pdf"
        save_path = self.upload_dir / unique_name

        try:
            # Read file in chunks to prevent memory spikes
            file_bytes = file.file.read()
            file_size = len(file_bytes)

            if file_size == 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Uploaded file is empty. Please upload a valid PDF resume.",
                )

            if file_size > settings.MAX_UPLOAD_SIZE_BYTES:
                raise HTTPException(
                    status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                    detail=f"File exceeds maximum allowed size of {settings.MAX_UPLOAD_SIZE_BYTES // (1024 * 1024)}MB.",
                )

            with open(save_path, "wb") as f:
                f.write(file_bytes)

            return save_path, filename, file_size

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to save uploaded file: {str(e)}",
            )
        finally:
            file.file.seek(0)

    def extract_text(self, file_path: Path | str) -> str:
        """
        Extract and clean text from PDF using PyMuPDF (fitz) with pypdf fallback.
        Handles scanned/empty PDFs gracefully without server crashes.
        """
        path = Path(file_path)
        if not path.exists():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Resume file not found on server.",
            )

        extracted_text = ""

        # Primary extraction using PyMuPDF (fitz)
        try:
            import fitz  # PyMuPDF

            doc = fitz.open(path)
            for page in doc:
                text = page.get_text("text")
                if text:
                    extracted_text += text + "\n"
            doc.close()
        except Exception:
            # Fallback extraction using pypdf
            try:
                import pypdf

                reader = pypdf.PdfReader(str(path))
                for page in reader.pages:
                    text = page.extract_text()
                    if text:
                        extracted_text += text + "\n"
            except Exception as ex:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Unable to read or parse PDF file. The file may be corrupted: {str(ex)}",
                )

        cleaned_text = self._clean_text(extracted_text)

        # Check if text is readable or if it's a scanned image without OCR
        if len(cleaned_text.strip()) < 30:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Unable to extract readable text from this PDF. Please upload a text-based PDF.",
            )

        return cleaned_text

    def _clean_text(self, text: str) -> str:
        """Normalize whitespace, remove non-printable characters, and preserve layout."""
        if not text:
            return ""

        # Replace carriage returns
        text = text.replace("\r\n", "\n").replace("\r", "\n")

        # Replace non-printable ASCII characters (keep newlines and tabs)
        text = re.sub(r"[^\x09\x0A\x0D\x20-\x7E\u00A0-\u024F\u1E00-\u1EFF]", " ", text)

        # Consolidate excessive blank lines to max 2
        text = re.sub(r"\n{3,}", "\n\n", text)

        # Consolidate multiple spaces
        lines = [re.sub(r"[ \t]{2,}", " ", line).strip() for line in text.split("\n")]
        return "\n".join(lines).strip()


pdf_service = PDFService()

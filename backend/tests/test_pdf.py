import io
from fastapi import UploadFile, HTTPException
import pytest
from app.services.pdf_service import PDFService


def test_invalid_extension(tmp_path):
    service = PDFService(upload_dir=tmp_path)
    file = UploadFile(filename="resume.txt", file=io.BytesIO(b"Some text"))
    with pytest.raises(HTTPException) as exc_info:
        service.validate_and_save(file)
    assert exc_info.value.status_code == 400
    assert "Only PDF files" in exc_info.value.detail


def test_empty_file(tmp_path):
    service = PDFService(upload_dir=tmp_path)
    file = UploadFile(filename="empty.pdf", file=io.BytesIO(b""))
    with pytest.raises(HTTPException) as exc_info:
        service.validate_and_save(file)
    assert exc_info.value.status_code == 400
    assert "empty" in exc_info.value.detail

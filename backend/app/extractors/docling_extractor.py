from docling.document_converter import DocumentConverter
import os

_converter = DocumentConverter()


def extract_html_from_file(file_path: str) -> str:
    """
    Use Docling to convert the given file_path (PDF/DOCX/etc.) into an HTML string.
    """
    result = _converter.convert(file_path)
    html = result.document.export_to_html()
    return html


def save_html_to_disk(html_content: str, output_path: str) -> None:
    """
    Write the HTML string to a local file. Creates parent dirs if needed.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)

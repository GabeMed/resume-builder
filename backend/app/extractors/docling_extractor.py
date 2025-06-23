from docling.document_converter import DocumentConverter
import os

converter = DocumentConverter()


def extract_html_from_file(file_path: str) -> str:
    """
    Use Docling to convert the given file_path (PDF/DOCX/etc.) into an HTML string.
    If the file is already HTML, read it directly.
    """
    file_ext = os.path.splitext(file_path)[1].lower()

    if file_ext == ".html":
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    try:
        result = converter.convert(file_path)
        html = result.document.export_to_html()
        return html
    except Exception as e:
        print(f"Warning: Docling extraction failed for {file_path}: {e}")
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                return f"<html><body><pre>{content}</pre></body></html>"
        except:
            return f"<html><body><p>Error: Could not extract content from {file_path}</p></body></html>"


def save_html_to_disk(html_content: str, output_path: str) -> None:
    """
    Write the HTML string to a local file. Creates parent dirs if needed.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)

from weasyprint import HTML


def generate_pdf(revised_html: str, output_path: str):
    HTML(string=revised_html).write_pdf(output_path)

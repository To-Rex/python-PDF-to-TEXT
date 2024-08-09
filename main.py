from flask import Flask, abort
import pdfplumber
import requests
from io import BytesIO

app = Flask(__name__)

pdf_cache = {}


@app.route('/<int:page_number>')
def pdf_page(page_number):
    pdf_url = "https://ildizkitoblari.uz/public/files/pdf1.pdf"
    try:
        if pdf_url not in pdf_cache:
            response = requests.get(pdf_url)
            response.raise_for_status()
            pdf_cache[pdf_url] = BytesIO(response.content)
        with pdfplumber.open(pdf_cache[pdf_url]) as pdf:
            total_pages = len(pdf.pages)
            if 1 <= page_number <= total_pages:
                page = pdf.pages[page_number - 1]
                text = page.extract_text()
                return text if text else "No text found on this page."
            else:
                abort(404, description=f"Page not found. The document has {total_pages} pages.")
    except requests.exceptions.RequestException as e:
        abort(500, description=f"Error fetching PDF: {str(e)}")
    except Exception as e:
        abort(500, description=str(e))


if __name__ == '__main__':
    app.run()

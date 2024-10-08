from io import BytesIO
import pdfplumber
import requests
from flask import Flask, abort, jsonify

app = Flask(__name__)

pdf_cache = {}

@app.route('/')
def hello_world():
    return 'Hello, World!'


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
                return jsonify({"text": text, "page": page_number}) if text else jsonify({"text": "No text found on this page.", "page": page_number})
            else:
                abort(404, description=f"Page not found. The document has {total_pages} pages.")
    except requests.exceptions.RequestException as e:
        abort(500, description=f"Error fetching PDF: {str(e)}")
    except Exception as e:
        abort(500, description=str(e))


@app.route('/pdf/')
def fetch_all_pdf():
    pdf_url = "https://ildizkitoblari.uz/public/files/pdf1.pdf"
    try:
        if pdf_url not in pdf_cache:
            response = requests.get(pdf_url)
            response.raise_for_status()
            pdf_cache[pdf_url] = BytesIO(response.content)
        with pdfplumber.open(pdf_cache[pdf_url]) as pdf:
            text = ""
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
            return jsonify({"text": text}) if text else jsonify({"text": "No text found in the document."})
    except requests.exceptions.RequestException as e:
        abort(500, description=f"Error fetching PDF: {str(e)}")
    except Exception as e:
        abort(500, description=str(e))


@app.route('/all')
def fetch_all_pdf_page():
    pdf_url = "https://ildizkitoblari.uz/public/files/pdf1.pdf"
    try:
        if pdf_url not in pdf_cache:
            response = requests.get(pdf_url)
            response.raise_for_status()
            pdf_cache[pdf_url] = BytesIO(response.content)
        with pdfplumber.open(pdf_cache[pdf_url]) as pdf:
            total_pages = len(pdf.pages)
            book = []
            for page_number in range(1, total_pages+1):
                page = pdf.pages[page_number - 1]
                text = page.extract_text()
                book.append({"text": text, "page": page_number})
            return jsonify({"book": book, "appPages": total_pages})
    except requests.exceptions.RequestException as e:
        abort(500, description=f"Error fetching PDF: {str(e)}")
    except Exception as e:
        abort(500, description=str(e))


@app.route('/<path:url>/all')
def fetch_all_pdf_page_url(url):
    pdf_url = url
    try:
        if pdf_url not in pdf_cache:
            response = requests.get(pdf_url)
            response.raise_for_status()
            pdf_cache[pdf_url] = BytesIO(response.content)
        with pdfplumber.open(pdf_cache[pdf_url]) as pdf:
            total_pages = len(pdf.pages)
            book = []
            for page_number in range(1, total_pages+1):
                page = pdf.pages[page_number - 1]
                text = page.extract_text()
                book.append({"text": text, "page": page_number})
            return jsonify({"book": book, "appPages": total_pages})
    except requests.exceptions.RequestException as e:
        abort(500, description=f"Error fetching PDF: {str(e)}")
    except Exception as e:
        abort(500, description=str(e))


@app.route('/pdf/<path:url>')
def fetch_all_pdf_page_url_all(url):
    pdf_url = url
    try:
        if pdf_url not in pdf_cache:
            response = requests.get(pdf_url)
            response.raise_for_status()
            pdf_cache[pdf_url] = BytesIO(response.content)
        with pdfplumber.open(pdf_cache[pdf_url]) as pdf:
            text = ""
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
            return jsonify({"text": text}) if text else jsonify({"text": "No text found in the document."})
    except requests.exceptions.RequestException as e:
        abort(500, description=f"Error fetching PDF: {str(e)}")
    except Exception as e:
        abort(500, description=str(e))


@app.route('/pdf/<path:url>/')
def fetch_pdf(url):
    pdf_url = url
    try:
        if pdf_url not in pdf_cache:
            response = requests.get(pdf_url)
            response.raise_for_status()
            pdf_cache[pdf_url] = BytesIO(response.content)
        with pdfplumber.open(pdf_cache[pdf_url]) as pdf:
            text = ""
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
            return jsonify({"text": text}) if text else jsonify({"text": "No text found in the document."})
    except requests.exceptions.RequestException as e:
        abort(500, description=f"Error fetching PDF: {str(e)}")
    except Exception as e:
        abort(500, description=str(e))


@app.route('/pdf/', defaults={'page_number': 1})
@app.route('/pdf/<path:url>/<int:page_number>')
def fetch_pdf_page(url, page_number):
    pdf_url = url
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
                return jsonify({"text": text, "page": page_number}) if text else jsonify({"text": "No text found on this page.", "page": page_number})
            else:
                abort(404, description=f"Page not found. The document has {total_pages} pages.")
    except requests.exceptions.RequestException as e:
        abort(500, description=f"Error fetching PDF: {str(e)}")
    except Exception as e:
        abort(500, description=str(e))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

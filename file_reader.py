from flask import Flask, request, jsonify
import csv
import mimetypes
import os
import fitz  # PyMuPDF
from PIL import Image
import base64
import io

app = Flask(__name__)

def read_text_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def read_csv_file(file_path):
    rows = []
    with open(file_path, mode='r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            rows.append(row)
    return '\n'.join([','.join(row) for row in rows])

def read_image_file(file_path):
    with open(file_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')

def read_pdf_file(file_path):
    text = []
    with fitz.open(file_path) as doc:
        for page in doc:
            text.append(page.get_text())
    return '\n'.join(text)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    # Temporarily save the file to process
    file_path = f"{file.filename}"
    file.save(file_path)
    
    # Identify the MIME type of the file
    mime_type, _ = mimetypes.guess_type(file_path)
    
    if mime_type is None:
        return jsonify({"error": "Unsupported file type or unable to detect file type."}), 400
    
    # Initialize the response content
    content = ""
    try:
        # Process based on MIME type
        if 'text' in mime_type:
            content = read_text_file(file_path)
        elif 'csv' in mime_type:
            content = read_csv_file(file_path)
        elif mime_type.startswith('image'):
            content = read_image_file(file_path)
            mime_type = "image/base64"
        elif 'pdf' in mime_type:
            content = read_pdf_file(file_path)
        else:
            return jsonify({"error": f"Unsupported file type: {mime_type}"}), 400
    finally:
        # Clean up: remove the temporarily saved file
        os.remove(file_path)
    
    return jsonify({"mime_type": mime_type, "content": content}), 200

if __name__ == '__main__':
    # Ensure the temp directory exists
    os.makedirs('./temp', exist_ok=True)
    app.run(debug=True)


import csv
import mimetypes
import os
import fitz  # PyMuPDF
from PIL import Image
import base64
import io
from openai import OpenAI
import requests

# Code Generation with OpenAI
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("OPENAI_API_KEY environment variable not set")

client = OpenAI(api_key=api_key)

# File Reading Functions
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

def process_file(file_path):
    mime_type, _ = mimetypes.guess_type(file_path)
    
    if mime_type is None:
        return "Unsupported file type or unable to detect file type."
    
    if 'text' in mime_type:
        return read_text_file(file_path)
    elif 'csv' in mime_type:
        return read_csv_file(file_path)
    elif mime_type.startswith('image'):
        return read_image_file(file_path)
    elif 'pdf' in mime_type:
        return read_pdf_file(file_path)
    else:
        return f"Unsupported file type: {mime_type}"




def generate_code(file, prompt, file_path):
    if not prompt:
        return 'No prompt provided', 400

    content = f"This is the prompt by the user - {prompt}, give python code which will be executed {prompt} and this is the file {file} ONLY GIVE CODE, NO TEXT WHATSOEVER"
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": content}
        ]
    )

    generated_code = completion.choices[0].message.content
    generated_code = generated_code.replace("```python\n", "").replace("\n```", "").strip()
    return generated_code

def send_code_to_execute(code):
    url = 'http://34.66.196.174:8085/execute'
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}  # Adjust content type for form data
    data = {'code': code}  # Include the code in the form data
    response = requests.post(url, data=data, headers=headers)
    return response.json()



#ENTER FILE PATH BECAUSE IT IS GETTING THAT WRONG
file = process_file("/Users/amir/Desktop/own-interpreter/interpret/lib/python3.11/site-packages/MyResume_1700764324.pdf")
generated_code = generate_code(file, "Please analyse this file")
execution_result = send_code_to_execute(generated_code)

print("The generated code is:", generated_code)
print("The type of generated code is ", type(generated_code))
print("Execution result:", execution_result)

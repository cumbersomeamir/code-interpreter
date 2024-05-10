import csv
import mimetypes
import os
import fitz  # PyMuPDF
from PIL import Image
import base64
import io
from openai import OpenAI
import requests


'''Initialising OpenAI API'''

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("OPENAI_API_KEY environment variable not set")

client = OpenAI(api_key=api_key)

'''File Reading Functions'''
#Reading Text File
def read_text_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()
#Reading CSV File
def read_csv_file(file_path):
    rows = []
    with open(file_path, mode='r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            rows.append(row)
    return '\n'.join([','.join(row) for row in rows])
    
#Reading Image File
def read_image_file(file_path):
    with open(file_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')

#Reading PDF File
def read_pdf_file(file_path):
    text = []
    with fitz.open(file_path) as doc:
        for page in doc:
            text.append(page.get_text())
    return '\n'.join(text)
    
#Processing the relevant file
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

'''Generating relevant code based on file_head, prompt, file_path'''

def generate_code(file_head, prompt, file_path):
    if not prompt:
        return 'No prompt provided', 400

    content = f"This is the prompt by the user - {prompt}, this is how the initial 5 lines of the file look like {file} and this is the filename {file_path} . PLEASE ONLY GIVE PYTHON CODE, NO TEXT WHATSOEVER"
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

''' Sending the code for execution'''
def send_code_and_file_to_execute(code, file_path):
    url = 'http://192.168.29.11:8085/execute'
    headers = {'Content-Type': 'multipart/form-data'}  # This header is typically managed by requests internally when using files param
    
    # Open the file in binary mode for uploading
    with open(file_path, 'rb') as f:
        files = {
            'file': (os.path.basename(file_path), f, mimetypes.guess_type(file_path)[0]),  # Guess the MIME type and attach
            'code': (None, code, 'text/plain')  # Send code as plain text
        }
        response = requests.post(url, files=files)
        
    return response.json()

print("all functions defined")



prompt = "Please analyse this file"
directory = "/Users/amir/Desktop/codeinterpreter/lib/python3.11/site-packages/Code interpreter test.csv"
base_name = os.path.basename(directory)
print("all initialisations done")

file = process_file(directory)
print("file processed")
file_head = file
generated_code = generate_code(file_head, prompt, base_name)
print("code generated")
execution_result = send_code_and_file_to_execute(generated_code, directory)
print("code executed")

print("The generated code is:", generated_code)
print("The type of generated code is ", type(generated_code))
print("Execution result:", execution_result)


#ENTER FILE PATH BECAUSE IT IS GETTING THAT WRONG
#1 - Extract name of the file
#2 - Append the extracted name of the file to pwd
#3 - CXhange code for extracting only the first 5 lines from the file, instead of the whole file
#4 Handle the executed result (What forms can it take?)

import csv
import mimetypes
import os
import fitz  # PyMuPDF
from PIL import Image
import base64
import io
from openai import OpenAI
import requests
import pandas as pd

#Initialising datatype
data_type = ""

'''Initialising OpenAI API'''

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("OPENAI_API_KEY environment variable not set")

client = OpenAI(api_key=api_key)

#Determining the file type
def get_extension_from_path(file_path):
    # Reverse the file path to start checking from the end
    reversed_path = file_path[::-1]
    
    # Find the first occurrence of a period in the reversed path
    dot_index = reversed_path.find('.')
    
    # If there's no period, return an empty string or indicate no extension
    if dot_index == -1:
        return "No extension found"
    
    # Extract the substring from the start to the dot index
    # Then reverse it back to normal
    extension = reversed_path[:dot_index][::-1]
    
    return extension

# Example usage
file_path = "/path/to/your/file.txt"
extension = get_extension_from_path(file_path)
print("File extension:", extension)


'''File Reading Functions'''
#Reading Text File
def read_text_file(file_path):
    data_type = 'text'
    with open(file_path, 'r') as file:
        return file.read()
        
# Reading CSV File
def read_csv_file(file_path):
    data_type = 'csv'
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(file_path, nrows=5)  # Read only the first 5 rows

    # Convert the DataFrame to a list of lists
    rows = df.values.tolist()
    print("FILE READ AS CSV")

    return rows
    
#Reading Image File
def read_image_file(file_path):
    data_type = 'image'
    with open(file_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')

#Reading PDF File
def read_pdf_file(file_path):
    data_type='pdf'
    text = []
    with fitz.open(file_path) as doc:
        for page in doc:
            text.append(page.get_text())
    return '\n'.join(text)
    
#Processing the relevant file
def process_file(file_path):
    
    if extension is None:
        return "Unsupported file type or unable to detect file type."
    
    elif extension == 'txt':
        return read_text_file(file_path)
    elif extension == 'csv':
        return read_csv_file(file_path)
    elif extension == 'png':
        return read_image_file(file_path)
    elif extension == 'pdf':
        return read_pdf_file(file_path)
    else:
        return f"Unsupported file type: {mime_type}"

'''Generating relevant code based on file_head, prompt, file_path'''

def generate_code(file_head, prompt, file_path):
    if not prompt:
        return 'No prompt provided', 400
    if data_type == 'csv':
        df = pd.read_csv(file_path)
        columns = df.columns
        print("the columns are ", columns)
        content = f"This is the prompt by the user - {prompt}, this is how the initial 5 lines of the file look like {file} and this is the filename {file_path} , the columns are {columns} . PLEASE ONLY GIVE PYTHON CODE, NO TEXT WHATSOEVER"
        completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You only generate python code for advanced analysis"},
            {"role": "user", "content": content}
        ]
    )
        generated_code = completion.choices[0].message.content
        generated_code = generated_code.replace("```python\n", "").replace("\n```", "").strip()
        return generated_code
    
    else:
        content = f"This is the prompt by the user - {prompt}, this is how the initial 5 lines of the file look like {file} and this is the filename {file_path} . PLEASE ONLY GIVE PYTHON CODE, NO TEXT WHATSOEVER"
        completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You only generate python code for advanced analysis"},
            {"role": "user", "content": content}
        ]
    )
    generated_code = completion.choices[0].message.content
    generated_code = generated_code.replace("```python\n", "").replace("\n```", "").strip()
    return generated_code
    

''' Sending the code for execution'''
def send_code_and_file_to_execute(code, file_path):
    url = 'http://192.168.1.7:8085/execute'
    headers = {'Content-Type': 'multipart/form-data'}  # This header is typically managed by requests internally when using files param
    
    # Open the file in binary mode for uploading
    with open(file_path, 'rb') as f:
        files = {
            'file': (os.path.basename(file_path), f, mimetypes.guess_type(file_path)[0]),  # Guess the MIME type and attach
            'code': (None, code, 'text/plain')  # Send code as plain text
        }
        response = requests.post(url, files=files)
        
    return response.json()
    
def generate_result(prompt, execution_result):
    if not prompt:
        return 'No prompt provided', 400

    content = f"This is the prompt by the user {prompt} and this is the result by the code interpreter {execution_result}. Can you create the short answer from the findings"
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Final Answer creator"},
            {"role": "user", "content": content}
        ]
    )
    final_answer = completion.choices[0].message.content
    return final_answer

print("all functions defined")

#Initialising the prompt
prompt = "Give me 3 insights from this data"
#Initialising the directory
directory = "/Users/amir/Desktop/codeinterpreter/lib/python3.11/site-packages/Code interpreter test.csv"
#Extracting the base name
base_name = os.path.basename(directory)

print("all initialisations done")
#Reading the file
file = process_file(directory)

print("file processed")
file_head = file
#Generating the code
generated_code = generate_code(file_head, prompt, base_name)
print("code generated")
#Executing the code
execution_result = send_code_and_file_to_execute(generated_code, directory)
print("code executed")
#Creating the final answer
final_result = generate_result(prompt, execution_result)


print("The generated code is:", generated_code)
print("The type of generated code is ", type(generated_code))
print("Execution result:", execution_result)
print("The final asnwer is ", final_result)


#ENTER FILE PATH BECAUSE IT IS GETTING THAT WRONG
#1 - Extract name of the file
#2 - Append the extracted name of the file to pwd
#3 - CXhange code for extracting only the first 5 lines from the file, instead of the whole file
#4 Handle the executed result (What forms can it take?)
#5 Install libraries which are not installed
#function calling - not needed
# Depreciation
# Documentation
# Memory
#Conditionally call all files type functions
# if 'text' in mime_type: - if file type is csv, also send the column names and then appened them to the prompt
#Find out the file types of all the 

import requests

url = 'http://127.0.0.1:5000/execute'
files = {'file': open('/Users/amir/Desktop/code-interpreter/interpreter/lib/python3.11/site-packages/test.py', 'rb')}
response = requests.post(url, files=files)
print(response.json())



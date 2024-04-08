import requests
import json

# The URL where your Flask app is running
url = 'http://localhost:5000/generate_code'

# The prompt you want to send
data = {
    'prompt': 'Create code for creating a chart using matplotlib'
}

# Sending a POST request to the Flask app
response = requests.post(url, json=data)

# Checking if the request was successful
if response.status_code == 200:
    print("Success:")
    print(response.json())
else:
    print("Error:", response.status_code)
    print(response.json())

import requests

def call_omni_file_reader_api(file_path):
    url = 'http://127.0.0.1:8001/upload'
    files = {'file': (file_path, open(file_path, 'rb'))}

    try:
        response = requests.post(url, files=files)
        response.raise_for_status()  # Raises a HTTPError if the response status code is 4XX/5XX
        return response.json()
    except requests.exceptions.HTTPError as errh:
        return f"Http Error: {errh}"
    except requests.exceptions.ConnectionError as errc:
        return f"Error Connecting: {errc}"
    except requests.exceptions.Timeout as errt:
        return f"Timeout Error: {errt}"
    except requests.exceptions.RequestException as err:
        return f"Oops: Something Else: {err}"

# Example usage
file_path = '/Users/amir/Desktop/code-interpreter/interpreter/lib/python3.11/site-packages/test.txt'
result = call_omni_file_reader_api(file_path)
print(result)



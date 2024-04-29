from flask import Flask, request, jsonify
import os
from openai import OpenAI


# Attempt to read the API key from the environment variable
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("OPENAI_API_KEY environment variable not set")



app = Flask(__name__)
client = OpenAI(api_key=api_key)

@app.route('/generate_code', methods=['POST'])
def generate_code():
    # Extract prompt from the request
    data = request.json
    prompt = data.get('prompt')

    if not prompt:
        return jsonify({'error': 'No prompt provided'}), 400

    content = f"This is the prompt by the user, give python code which will be executed {prompt} Only give code, no text whatsoever"
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": content}
        ]
    )

    # Extracting the generated code from the response
    generated_code = completion.choices[0].message.content
    
    # Remove Markdown backticks
    generated_code = generated_code.replace("```python\n", "").replace("\n```", "").strip()

    # Return the generated code as a response
    return jsonify({'generated_code': generated_code})

if __name__ == '__main__':
    app.run(debug=True, port=8085)

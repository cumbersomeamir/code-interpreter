from flask import Flask, request, jsonify
import os
from openai import OpenAI

#Update code for input using terminal
os.environ["OPENAI_API_KEY"] = ""

app = Flask(__name__)
client = OpenAI()

@app.route('/generate', methods=['POST'])
def generate_text():
    try:
        completion = client.chat.completions.create(
          model="gpt-3.5-turbo",
          messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello!"}
          ]
        )

        generated_text = completion.choices[0].message
        print("The generated text is", generated_text)
        
        # Return the generated text
        return jsonify({"generated_text": generated_text})
    
    except Exception as e:
        # In case of any error, return an error message
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)


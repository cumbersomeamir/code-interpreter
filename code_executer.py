from flask import Flask, request, jsonify
import subprocess
import os
import uuid


app = Flask(__name__)

@app.route('/execute', methods = ['POST'])

def execute_python_code():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file and file.filename.endswith('.py'):
        filename = str(uuid.uuid4()) + '.py'
        filepath = os.path.join('/tmp', filename)
        file.save(filepath)
        try:
        
            result = subprocess.run(['python', filepath], capture_output=True, text=True, timeout=30)
            os.remove(filepath) #Clean up the file after execution
            return jsonify({"output": result.stdout, "error": result.stderr}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
            
if __name__ == '__main__':
    app.run(debug=True, port=8083)
    

    

from flask import Flask, request, jsonify
import subprocess
import os
import tempfile  # Use tempfile to manage temporary files securely

app = Flask(__name__)

# Endpoint to execute code securely with an optional file upload
@app.route('/execute', methods=['POST'])
def execute_code():
    code = request.form.get('code')
    uploaded_file = request.files.get('file')
    
    if not code:
        return jsonify({"error": "No code provided"}), 400

    # Manage a temporary directory for code and file
    with tempfile.TemporaryDirectory() as temp_dir:
        # Save the code to a temporary Python file
        temp_code_path = os.path.join(temp_dir, "temp_code_to_execute.py")
        with open(temp_code_path, 'w') as file:
            file.write(code)

        # Save the uploaded file if present
        if uploaded_file:
            file_path = os.path.join(temp_dir, uploaded_file.filename)
            uploaded_file.save(file_path)
        
        # Execute the Python file in a separate process
        try:
            result = subprocess.run(['python', temp_code_path], capture_output=True, text=True, timeout=30)
            if result.returncode == 0:
                return jsonify({"output": result.stdout}), 200
            else:
                return jsonify({"error": result.stderr}), 400
        except subprocess.TimeoutExpired:
            return jsonify({"error": "Execution timed out"}), 500
        except Exception as e:
            return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8085)

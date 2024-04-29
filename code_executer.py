from flask import Flask, request, jsonify
import subprocess
import os

app = Flask(__name__)

# Endpoint to execute code securely
@app.route('/execute', methods=['POST'])
def execute_code():
    code = request.form.get('code')
    
    if not code:
        return jsonify({"error": "No code provided"}), 400
    
    # Save the code to a temporary Python file
    temp_file = "temp_code_to_execute.py"
    with open(temp_file, 'w') as file:
        file.write(code)
    
    # Execute the Python file in a separate process
    try:
        result = subprocess.run(['python', temp_file], capture_output=True, text=True, timeout=30)
        os.remove(temp_file)  # Clean up the temporary file
        if result.returncode == 0:
            return jsonify({"output": result.stdout}), 200
        else:
            return jsonify({"error": result.stderr}), 400
    except subprocess.TimeoutExpired:
        return jsonify({"error": "Execution timed out"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host= '0.0.0.0', port=8085)


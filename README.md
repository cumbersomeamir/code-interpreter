**Flow:**
User inputs prompt and file->
File Reader->
Code Writer->
Code Executer->
Vanilla LLM->
<img width="368" alt="Screenshot 2024-04-08 at 15 58 23" src="https://github.com/cumbersomeamir/code-interpreter/assets/40836125/3656966b-f73c-4bdf-a24b-8ce1e824423c">


Further Implementations:

1. Sandboxing: Run the code in a sandboxed environment to limit its access to the system. This can be achieved with Docker containers or dedicated virtual machines.
2. Resource Limits: Implement limits on CPU time and memory usage to prevent denial-of-service attacks.
3. Input Sanitization: Although difficult with direct code execution, ensure that inputs are checked or sanitized as much as possible.
4. Monitoring and Logging: Keep detailed logs and monitor the execution of submitted scripts for any unusual activity.

**Test Endpoints**

Write Code:
curl -X POST http://127.0.0.1:5000/generate_code -H "Content-Type: application/json" -d "{\"prompt\":\"Create a sample chart using matplotlib\"}"

curl -X POST -F "file=@/Users/amir/Desktop/code-interpreter/interpreter/lib/python3.11/site-packages/test.py" http://127.0.0.1:5000/execute

**Flow:**
User inputs prompt and file->
File Reader->
Code Writer->
Code Executer->
Vanilla LLM->


<img width="381" alt="Screenshot 2024-04-09 at 19 27 42" src="https://github.com/cumbersomeamir/code-interpreter/assets/40836125/c09d3000-57f6-4176-9a11-7de1de66aa06">
# Add code for exporting different files too

Further Implementations:

1. Sandboxing: Run the code in a sandboxed environment to limit its access to the system. This can be achieved with Docker containers or dedicated virtual machines.
2. Resource Limits: Implement limits on CPU time and memory usage to prevent denial-of-service attacks.
3. Input Sanitization: Although difficult with direct code execution, ensure that inputs are checked or sanitized as much as possible.
4. Monitoring and Logging: Keep detailed logs and monitor the execution of submitted scripts for any unusual activity.

**Test Endpoints**

Write Code:
curl -X POST http://127.0.0.1:5000/generate_code -H "Content-Type: application/json" -d "{\"prompt\":\"Create a sample chart using matplotlib\"}"

curl -X POST -F "file=@/Users/amir/Desktop/code-interpreter/interpreter/lib/python3.11/site-packages/test.py" http://127.0.0.1:5000/execute



**pip install**
pip3 install PyMuPDF openai requests Pillow


Need to install all libraries in the code_executer also for making the code work

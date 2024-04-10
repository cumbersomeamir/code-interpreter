import streamlit as st
import requests
import os
import openai

# Read the API key from the environment variable
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("OPENAI_API_KEY environment variable not set")

# Initialize the OpenAI client
client = openai.OpenAI(api_key=api_key)

def create_final_answer(prompt, executed_output):
    content = f"This is the prompt by the user: '{prompt}' and this is the executed code output given by the code interpreter: '{executed_output}', please create the final answer."
    response = client.chat_completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": content}
        ]
    )

    # Extracting the generated code from the response
    final_answer = response.choices[0].message['content']
    return final_answer

def main():
    st.title("Streamlit Prompt and File Upload Example")

    prompt = st.text_input("Enter your prompt", "")
    uploaded_file = st.file_uploader("Choose a file")

    if prompt and uploaded_file:
        st.write(f"Entered prompt: {prompt}")
        st.write(f"Uploaded file: {uploaded_file.name}")

        files = {'file': (uploaded_file.name, uploaded_file, uploaded_file.type)}
        file_reader_response = requests.post('http://127.0.0.1:8081/upload', files=files)

        if file_reader_response.status_code == 200:
            file_content = file_reader_response.json()['content']

            code_writer_response = requests.post(
                'http://127.0.0.1:8082/generate_code',
                json={'prompt': prompt + " " + file_content}
            )

            if code_writer_response.status_code == 200:
                generated_code = code_writer_response.json()['generated_code']

                executer_files = {'file': ('code.py', generated_code, 'text/plain')}
                code_executer_response = requests.post('http://127.0.0.1:8083/execute', files=executer_files)

                if code_executer_response.status_code == 200:
                    executed_output = code_executer_response.json()
                    output = executed_output.get('output', '')
                    error = executed_output.get('error', '')

                    if error:
                        st.write(f"Execution Error: {error}")
                    else:
                        st.write(f"Executed Output: {output}")

                        # Create the final answer using the OpenAI API
                        final_answer = create_final_answer(prompt, output)
                        st.write(f"Final Answer: {final_answer}")

                else:
                    st.error("Error calling the code executor API")
            else:
                st.error("Error calling the code writer API")
        else:
            st.error("Error calling the file reader API")

if __name__ == "__main__":
    main()

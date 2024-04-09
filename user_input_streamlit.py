import streamlit as st

def main():
    # Set the title of the web app
    st.title("Streamlit Prompt and File Upload Example")

    # Text input for the prompt
    prompt = st.text_input("Enter your prompt", "")

    # File uploader allows the user to upload files
    uploaded_file = st.file_uploader("Choose a file")

    # Display the prompt and file name if a file was uploaded
    if prompt:
        st.write(f"Entered prompt: {prompt}")

    if uploaded_file is not None:
        st.write(f"Uploaded file: {uploaded_file.name}")

if __name__ == "__main__":
    main()


#Vanilla LLM : Create Final Answer

import os
from openai import OpenAI


# Attempt to read the API key from the environment variable
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("OPENAI_API_KEY environment variable not set")




client = OpenAI(api_key=api_key)


def create_final_answer(prompt, executed_output):
    


    content = f"This is the prompt by the user{prompt} and this is the executed code output given by code interpreter {executed_output}, please create the final answer"
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": content}
        ]
    )

    # Extracting the generated code from the response
    generated_code = completion.choices[0].message.content
    
    print(generated_code)
    

create_final_answer("What is happen in this file", "Unnamed: 0 DOCUMENTS REQUIRED     Unnamed: 2 0        NaN                 NaN           NaN")
    

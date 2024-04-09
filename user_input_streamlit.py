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

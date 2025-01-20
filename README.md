# Summary Generation
- # Installation
    - Clone the directory, pass the file path in the 
    `main.py` file.
    - make a `.env` file and mention the following parameters in it 
        - AZURE_DEPLOYMENT_NAME=
        - AZURE_MODEL_NAME=
        - AZURE_OPENAI_API_KEY=
        - AZURE_API_VERSION=
        - AZURE_USER_ID=
        - AZURE_OPENAI_ENDPOINT=
    - Run the `requirements.txt` file using 
        ```bash
        pip install -r requirements.txt
        ```

    - Now either you can run the `streamlit.py` file using 
        ```bash
        streamlit run streamlit.py
        ```
        or run `develop.py` file by calling `json_resp` function in it.

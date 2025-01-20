import streamlit as st
from main import count_tokens, text as extracted_text
from develop import json_resp

def main():
    # intent = GetQueryIntent().get_query_intent("secondment case laws")
    # print(type(intent), intent)
    # document_source_2 = ["Vat_infoline_db", "Bharat_laws_db", "Taxsutra_db"]
    # distinct_folders = FolderLibraryHandler().get_folder_from_document_source(document_source_2)
    # query = "7 Judgements on GST"
    # folder_intent = FolderLibraryHandler().query_intents_v2(query, distinct_folders)
    # print(type(folder_intent), folder_intent)
    # obj = AzureChatOpenAI4o(max_tokens=1000, temperature=0.0).llm
    # print(obj)
    # print(obj.invoke("What is the capital of Australia?"))
    # embedder = CreateEmbeddings()
    # print(embedder.embedder)
    # etext = embedder.embedder.embed_query('hi')
    # print(etext[:3])
    # llm = CustomAzureChatOpenAI(max_tokens=3000, temperature=0).llm
    # print(llm)
    st.title("PDF Reader")
    st.write("Upload a PDF file.")
    # handler = QuerySugestionProcess()
    query = "5 documents of GST case laws on secondment"
    print(query)
    # print(handler.getSuggestedQueriesForGivenQuery(query=query, client_id=""))

    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    if uploaded_file is not None:
        st.success("File uploaded successfully!")
        with st.spinner("Processing PDF..."):
            # extracted_text = read_pdf(uploaded_file) # Process pdf from upload
            # extracted_text = read_pdf_pypdf()
            # Getting tokens 
            num_tokens = count_tokens(extracted_text)
            print("number of tokens in doc: %s" % num_tokens)
            # print(extracted_text)
        
        if extracted_text:
            st.subheader("Extracted PDF Content:")
            st.text_area("Output", extracted_text, height=500)
            # print(extracted_text)
            
            user_query = st.text_area("Enter your query", height=100)

            if st.button("Summarize") or user_query:
                # if user_query.strip():
                with st.spinner("Generating..."):
                    # answer = await summarize_text(extracted_text)
                    # answer = parallel_summary(extracted_text)
                    # print(extracted_text)

                    answer, answer_other_info, answer_references_info = json_resp(extracted_text)
                    st.subheader("Answer:")
                    st.subheader("Brief overall summary")
                    st.write(answer)
                    st.subheader("Brief other information of the case")
                    st.write(answer_other_info)
                    st.subheader("Brief references in the case")
                    st.write(answer_references_info)
            else:
                st.warning("Please enter some text to Query.")

if __name__ == "__main__":
    main()
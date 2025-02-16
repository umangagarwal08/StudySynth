import streamlit as st
from rag import rag_pdf, answer_generator 




st.title("AI-Powered PDF Study Assistant")
uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

if uploaded_file is not None:
    st.success("PDF uploaded successfully!")
    retrival=rag_pdf(uploaded_file)
    st.write("### Prerequisites Identified:")
    st.write()
    '''    
        confirm = st.checkbox("Proceed with generating study modules")
        
        if confirm:
            if st.button("Generate Modules"):
                with st.spinner("Generating study modules..."):
                    modules_text = generate_modules(text)
                    modules = modules_text.split("////////////////")
                    st.write("### Study Modules:")
                    for i, module in enumerate(modules, start=1):
                        with st.expander(f"Module {i}"):
                            st.write(module)
'''

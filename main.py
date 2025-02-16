import streamlit as st
from rag import rag_pdf, answer_generator 




st.title("AI-Powered PDF Study Assistant")
uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

if uploaded_file is not None:
    st.success("PDF uploaded successfully!")
    retrival=rag_pdf(uploaded_file)
    st.write("### Prerequisites Identified:")

    query="""Analyze the provided document and identify the three most essential prerequisite topics required to understand it. List only the topic names in order of importance, without any explanations.

    For example, if the document is about Convolutional Neural Networks (CNNs), the output should be:

    Python
    Deep Learning
    Computer Vision
    Ensure that the topics are listed in decreasing order of necessity comma seperated ."""
    result =answer_generator(retrival,query)
    prerequisitory = result.split(",")
    st.markdown(prerequisitory)


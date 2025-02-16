import streamlit as st
from rag import rag_pdf, answer_generator 




st.title("AI-Powered PDF Study Assistant")
uploaded_file = st.sidebar.file_uploader("Upload a PDF", type=["pdf"])

if uploaded_file is not None:
    st.sidebar.success("PDF uploaded successfully!")
    retrival=rag_pdf(uploaded_file)
    st.write("### The uploaded file requires some prerequisite knowledge. Please tick the items you are aware of so we can create the modules accordingly.")

    Prerequisites="""Analyze the provided document and identify the three most essential prerequisite topics required to understand it. List only the topic names in order of importance, without any explanations.

    For example, if the document is about Convolutional Neural Networks (CNNs), the output should be:

    Python
    Deep Learning
    Computer Vision
    Ensure that the topics are listed in decreasing order of necessity comma seperated ."""
    result =answer_generator(retrival,Prerequisites)
    Prerequisites = result.split(",")
    #st.markdown(prerequisitory)

    #st.title("Knowledge Checklist")
    #st.write("Tick the things that you already know and click submit.")

    # Dictionary to hold checkbox states
    selected_items = {}

    # Create checkboxes for each item
    for item in Prerequisites:
        selected_items[item] = st.checkbox(item)

    # Submit button
    if st.button("Submit"):
        known_items = [item for item, checked in selected_items.items() if checked]
    
        if known_items:
            st.success("You have selected the following:")
            st.write(known_items)
        else:
            st.warning("You didn't select anything.")


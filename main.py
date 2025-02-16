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

        Prerequisites_selected=selected_items.values()

        topic_query=f"""The user is familiar with the following prerequisite topics: {Prerequisites_selected} out of {Prerequisites}

            Now, based on the provided document, create a structured 5-module study plan that enables the user to deeply understand the content. Ensure that:

        Each module is highly detailed.
        The explanation considers what the user already knows and avoids redundant basic explanations of known prerequisites.
        Each module builds progressively, making it easy to grasp advanced concepts.
        The study material is engaging, well-structured, and includes real-world examples where applicable.
        put "?|?" in the last of each module"""

        result =answer_generator(retrival,topic_query)

        module=result.split("?|?")

        

        for i in range(1,6):
            module_query=f'''I am providing you with the module **{module[i-1]}**, based on the given document. Explain all the
            terms in this module in extreme detail, covering definitions, context, examples, and relevant background information. 
            Take most of the references from the document to ensure accuracy and alignment with the source material.'''
            st.title(f"Module {i}")
            result_q =answer_generator(retrival,module_query)
            st.markdown(result_q)








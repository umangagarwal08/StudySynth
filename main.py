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
    
    selected_items[Prerequisites[0]] = st.checkbox(Prerequisites[0])
    selected_items[Prerequisites[1]] = st.checkbox(Prerequisites[1])
    selected_items[Prerequisites[2]] = st.checkbox(Prerequisites[2])

    # Submit button
    pre_sub=st.button("Submit")

if pre_sub:
        
        
    Prerequisites_selected=selected_items.values()

    topic_query=f"""The user is familiar with the following prerequisite topics: {Prerequisites_selected} out of {Prerequisites}

            Now, based on the provided document, create a structured 5-module study plan that enables the user to deeply understand the content. Ensure that:

        Each module is highly detailed.
        The explanation considers what the user already knows and avoids redundant basic explanations of known prerequisites.
        Each module builds progressively, making it easy to grasp advanced concepts.
        The study material is engaging, well-structured, and includes real-world examples where applicable.
        put "?|?" in the last of each module"""

    result =answer_generator(retrival,topic_query)

    st.markdown(result)

    module=result.split("?|?")

    gen_button=st.button("Create Detailed Modules ")


if gen_button:
        
    if st.button("Module 1"):
            module_query=f'''I am providing you with the module **{module[0]}**, based on the given document. Explain all the
            terms in this module in extreme detail, covering definitions, context, examples, and relevant background information. 
            Take most of the references from the document to ensure accuracy and alignment with the source material.'''
            st.title(f"Module 1")
            result_1 =answer_generator(retrival,module_query)
            st.markdown(result_1)
    if st.button("Module 2"):
            module_query=f'''I am providing you with the module **{module[1]}**, based on the given document. Explain all the
            terms in this module in extreme detail, covering definitions, context, examples, and relevant background information. 
            Take most of the references from the document to ensure accuracy and alignment with the source material.'''
            st.title(f"Module 2")
            result_2 =answer_generator(retrival,module_query)
            st.markdown(result_2)
    if st.button("Module 3"):
            module_query=f'''I am providing you with the module **{module[2]}**, based on the given document. Explain all the
            terms in this module in extreme detail, covering definitions, context, examples, and relevant background information. 
            Take most of the references from the document to ensure accuracy and alignment with the source material.'''
            st.title(f"Module 3")
            result_3 =answer_generator(retrival,module_query)
            st.markdown(result_3)
    if st.button("Module 4"):
            module_query=f'''I am providing you with the module **{module[3]}**, based on the given document. Explain all the
            terms in this module in extreme detail, covering definitions, context, examples, and relevant background information. 
            Take most of the references from the document to ensure accuracy and alignment with the source material.'''
            st.title(f"Module 4")
            result_4 =answer_generator(retrival,module_query)
            st.markdown(result_4)
    if st.button("Module 5"):
            module_query=f'''I am providing you with the module **{module[4]}**, based on the given document. Explain all the
            terms in this module in extreme detail, covering definitions, context, examples, and relevant background information. 
            Take most of the references from the document to ensure accuracy and alignment with the source material.'''
            st.title(f"Module 5")
            result_5 =answer_generator(retrival,module_query)
            st.markdown(result_5)













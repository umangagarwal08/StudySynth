import streamlit as st
from rag import rag_pdf, answer_generator

st.title("AI-Powered PDF Study Assistant")

# File Upload Section
uploaded_file = st.sidebar.file_uploader("Upload a PDF", type=["pdf"])
if uploaded_file and st.sidebar.button("Submit PDF"):
    st.session_state.clear()
    st.session_state["file_uploaded"] = True
    st.session_state["retrieval"] = rag_pdf(uploaded_file)
    st.sidebar.success("PDF submitted successfully!")

# Initialize session state variables
session_defaults = {
    "prerequisites": [],
    "modules": [],
    "selected_module": None,
    "questions": {},
    "detailed_explanations": {}
}
for key, value in session_defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# Generate prerequisites
if st.session_state.get("file_uploaded") and not st.session_state["modules"]:
    st.write("### Select prerequisite topics you are familiar with:")
    prerequisite_query = """Identify three essential prerequisite topics required to understand this document, listed comma-separated."""
    st.session_state["prerequisites"] = answer_generator(st.session_state["retrieval"], prerequisite_query).split(",")

# Display Prerequisites
if st.session_state["prerequisites"]:
    selected_prerequisites = {}
    for topic in st.session_state["prerequisites"]:
        selected_prerequisites[topic] = st.checkbox(topic)

    
    if st.button("Submit Prerequisites"):
        known_topics = [topic for topic, checked in selected_prerequisites.items() if checked]
        study_plan_query = f"""
        The user is familiar with the following prerequisite topics: {selected_prerequisites} out of {st.session_state["prerequisites"]}.
        Now, based on the provided document, create a structured 5-module study plan that enables the user to deeply understand the content.
        Ensure that:
        - Each module is highly detailed.
        - The explanation considers what the user already knows and avoids redundant basic explanations.
        - Each module builds progressively.
        - The study material is well-structured and engaging.
        - Use "?|?" to separate each module.

Format:
Module 1: [Detailed Content] 
?|?  
Module 2: [Detailed Content] 
?|?  
Module 3: [Detailed Content] 
?|?  
Module 4: [Detailed Content] 
?|?  
Module 5: [Detailed Content]  

Ensure clarity, completeness, and proper structure for each module.
"""

        st.session_state["modules"] = answer_generator(st.session_state["retrieval"], study_plan_query).split("?|?")
        st.success("Study plan created successfully!")

# Display Study Plan
if st.session_state["modules"]:
    st.write("### Study Plan:")
    for i, module in enumerate(st.session_state["modules"], start=1):
        st.write(f"**Module {i}:** {module}")
    
    # Module Selection
    module_labels = [f"Module {i+1}" for i in range(len(st.session_state["modules"]))]
    selected_module_index = st.selectbox("Select a module:", list(range(len(module_labels))), format_func=lambda x: module_labels[x])
    
    # Generate Detailed Explanation
    if st.button("Generate Detailed Explanation"):
        if selected_module_index not in st.session_state["detailed_explanations"]:
            explanation_query = f"""
            Explain the module **{st.session_state["modules"][selected_module_index]}** in extreme detail with definitions, examples, and context from the document.
            """
            st.session_state["detailed_explanations"][selected_module_index] = answer_generator(st.session_state["retrieval"], explanation_query)
    
    # Display Explanation
    if selected_module_index in st.session_state["detailed_explanations"]:
        st.subheader(f"{module_labels[selected_module_index]} - Detailed Explanation")
        st.markdown(st.session_state["detailed_explanations"][selected_module_index])
    
    # Generate Questions
    if st.button("Generate Questions"):
        question_query = f"""
        Create 4-5 MCQs with answers and 4-5 theoretical questions for **{st.session_state["modules"][selected_module_index]}**.
        """
        st.session_state["questions"][selected_module_index] = answer_generator(st.session_state["retrieval"], question_query).split("\n")
    
    # Display Questions
    if selected_module_index in st.session_state["questions"]:
        st.write("### Questions:")
        for question in st.session_state["questions"][selected_module_index]:
            st.write(question)

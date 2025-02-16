import streamlit as st
from rag import rag_pdf, answer_generator 

st.title("AI-Powered PDF Study Assistant")

# Initialize session state
if "prerequisites" not in st.session_state:
    st.session_state.prerequisites = []
if "modules" not in st.session_state:
    st.session_state.modules = []
if "retrival" not in st.session_state:
    st.session_state.retrival = None
if "file_uploaded" not in st.session_state:
    st.session_state.file_uploaded = False
if "selected_module" not in st.session_state:
    st.session_state.selected_module = None
if "questions" not in st.session_state:
    st.session_state.questions = []

# File Upload Section
uploaded_file = st.sidebar.file_uploader("Upload a PDF", type=["pdf"])

# Submit button to confirm PDF upload
if uploaded_file:
    if st.sidebar.button("Submit PDF"):
        st.session_state.file_uploaded = True
        st.sidebar.success("PDF submitted successfully!")

# Process the PDF only after submission
if st.session_state.file_uploaded and uploaded_file is not None and st.session_state.retrival is None:
    st.session_state.retrival = rag_pdf(uploaded_file)

    st.write("### The uploaded file requires some prerequisite knowledge. Please tick the items you are aware of so we can create the modules accordingly.")

    prerequisite_query = """Analyze the provided document and identify the three most essential prerequisite topics required to understand it. 
    List only the topic names in order of importance, comma separated."""
    
    result = answer_generator(st.session_state.retrival, prerequisite_query)
    st.session_state.prerequisites = result.split(",")

# Display Prerequisites if available
if st.session_state.prerequisites:
    selected_items = {}

    for topic in st.session_state.prerequisites:
        selected_items[topic] = st.checkbox(topic)

    if st.button("Submit Prerequisites"):
        Prerequisites_selected = [topic for topic, checked in selected_items.items() if checked]

        study_plan_query = f"""
        The user is familiar with the following prerequisite topics: {Prerequisites_selected} out of {st.session_state.prerequisites}.
        Now, based on the provided document, create a structured 5-module study plan that enables the user to deeply understand the content.
        Ensure that:
        - Each module is highly detailed.
        - The explanation considers what the user already knows and avoids redundant basic explanations.
        - Each module builds progressively.
        - The study material is well-structured and engaging.
        - Use "?|?" to separate each module.
        """

        result = answer_generator(st.session_state.retrival, study_plan_query)
        st.session_state.modules = result.split("?|?")
        st.success("Study plan created successfully!")

# Display Modules if generated
if st.session_state.modules:
    st.write("### Study Plan:")
    for i, module in enumerate(st.session_state.modules):
        st.write(f"**Module {i+1}:** {module}")

    # Select a module
    st.session_state.selected_module = st.selectbox("Select a module:", [f"Module {i+1}" for i in range(len(st.session_state.modules))])
    
    if st.button("Generate Detailed Explanation"):
        module_index = int(st.session_state.selected_module.split(" ")[1]) - 1
        module_query = f"""
        I am providing you with the module **{st.session_state.modules[module_index]}**, based on the given document.
        Explain all terms in extreme detail, covering definitions, context, examples, and relevant background information. 
        Take most references from the document to ensure accuracy.
        """
        detailed_module = answer_generator(st.session_state.retrival, module_query)
        st.subheader(f"{st.session_state.selected_module} - Detailed Explanation")
        st.markdown(detailed_module)

# --- EVALUATION SECTION ---
st.sidebar.subheader("📌 Module Evaluation")

if st.session_state.selected_module:
    module_index = int(st.session_state.selected_module.split(" ")[1]) - 1
    
    if st.sidebar.button("Generate Questions"):
        question_query = f"""
        Based on **{st.session_state.modules[module_index]}**, create:
        - 4-5 multiple-choice questions (MCQs) with 4 answer options (mark the correct one).
        - 4-5 theoretical questions requiring written answers.
        """
        result = answer_generator(st.session_state.retrival, question_query)
        st.session_state.questions = result.split("\n")

    # Display generated questions if available
    if st.session_state.questions:
        st.sidebar.write("### Questions:")
        for q in st.session_state.questions:
            st.sidebar.write(q)

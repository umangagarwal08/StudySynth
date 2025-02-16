import streamlit as st
from rag import rag_pdf, answer_generator 

st.title("AI-Powered PDF Study Assistant")

# File Upload Section
uploaded_file = st.sidebar.file_uploader("Upload a PDF", type=["pdf"])

# Reset session state when a new PDF is submitted
if uploaded_file and st.sidebar.button("Submit PDF"):
    st.session_state.clear()  # Clears all previous session state values
    st.session_state["file_uploaded"] = True
    st.session_state["retrival"] = rag_pdf(uploaded_file)
    st.sidebar.success("PDF submitted successfully!")

# Initialize session state if not set
if "prerequisites" not in st.session_state:
    st.session_state["prerequisites"] = []
if "modules" not in st.session_state:
    st.session_state["modules"] = []
if "detailed_plan_generated" not in st.session_state:
    st.session_state["detailed_plan_generated"] = False
if "questions" not in st.session_state:
    st.session_state["questions"] = {}

# Process the PDF only after submission
if st.session_state.get("file_uploaded", False) and not st.session_state["modules"]:
    st.write("### The uploaded file requires some prerequisite knowledge. Please tick the items you are aware of so we can create the modules accordingly.")

    prerequisite_query = """Analyze the provided document and identify the three most essential prerequisite topics required to understand it. 
    List only the topic names in order of importance, comma separated."""
    
    result = answer_generator(st.session_state["retrival"], prerequisite_query)
    st.session_state["prerequisites"] = result.split(",")

# Display Prerequisites if available
if st.session_state["prerequisites"]:
    selected_items = {}

    for topic in st.session_state["prerequisites"]:
        selected_items[topic] = st.checkbox(topic)

    if st.button("Submit Prerequisites"):
        Prerequisites_selected = [topic for topic, checked in selected_items.items() if checked]

        study_plan_query = f"""
        The user is familiar with the following prerequisite topics: {Prerequisites_selected} out of {st.session_state["prerequisites"]}.
        Now, based on the provided document, create a structured 5-module study plan that enables the user to deeply understand the content.
        Ensure that:
        - Each module is highly detailed.
        - The explanation considers what the user already knows and avoids redundant basic explanations.
        - Each module builds progressively.
        - The study material is well-structured and engaging.
        - Use "?|?" to separate each module.
        """

        result = answer_generator(st.session_state["retrival"], study_plan_query)
        st.session_state["modules"] = result.split("?|?")
        st.success("Study plan created successfully!")

# Display Study Plan if generated
if st.session_state["modules"]:
    st.write("### Study Plan:")
    for i, module in enumerate(st.session_state["modules"]):
        st.write(f"**Module {i+1}:** {module}")

    # Generate Detailed Plan Button
    if st.button("Generate Detailed Plan"):
        st.session_state["detailed_plan_generated"] = True

# Display Module Details & Questions if detailed plan is generated
if st.session_state["detailed_plan_generated"]:
    st.write("### Detailed Study Plan")
    
    for i, module in enumerate(st.session_state["modules"]):
        with st.expander(f"**Module {i+1}:**"):
            # Generate detailed explanation if not already stored
            if f"module_{i+1}_details" not in st.session_state:
                module_query = f"""
                I am providing you with the module **{module}**, based on the given document.
                Explain all terms in extreme detail, covering definitions, context, examples, and relevant background information. 
                Take most references from the document to ensure accuracy.
                """
                st.session_state[f"module_{i+1}_details"] = answer_generator(st.session_state["retrival"], module_query)

            # Display the module details
            st.subheader(f"Module {i+1} - Detailed Explanation")
            st.markdown(st.session_state[f"module_{i+1}_details"])

            # Generate Questions Button
            if st.button(f"Generate Questions for Module {i+1}"):
                question_query = f"""
                Based on **{module}**, create:
                - 4-5 multiple-choice questions (MCQs) with 4 answer options (mark the correct one).
                - 4-5 theoretical questions requiring written answers.
                """
                st.session_state["questions"][f"module_{i+1}"] = answer_generator(st.session_state["retrival"], question_query).split("\n")

            # Display generated questions if available
            if f"module_{i+1}" in st.session_state["questions"]:
                st.write("### Questions:")
                for q in st.session_state["questions"][f"module_{i+1}"]:
                    st.write(q)

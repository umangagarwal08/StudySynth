# AI-Powered PDF Study Assistant

## Overview
The **AI-Powered PDF Study Assistant** is a Streamlit-based application that allows users to upload a PDF and generate a structured study plan. The app leverages **Retrieval-Augmented Generation (RAG)** techniques to extract relevant information, identify prerequisite knowledge, and create a tailored learning experience.

## Features
- **PDF Upload & Processing**: Users can upload a PDF, which is then processed to extract meaningful content.
- **Prerequisite Knowledge Identification**: The system determines essential prerequisite topics required to understand the document.
- **Custom Study Plan Generation**: A five-module study plan is created based on the user's knowledge and document content.
- **Detailed Module Explanations**: Each module is explained in-depth with definitions, examples, and context.
- **Question Generation**: Generates multiple-choice and theoretical questions for self-assessment.

## Tech Stack
- **Python**
- **Streamlit** (Frontend UI)
- **LangChain** (Retrieval-Augmented Generation)
- **FAISS** (Vector Database for efficient document retrieval)
- **HuggingFace Embeddings** (BAAI/bge-large-en model for text embeddings)
- **Mistral AI** (LLM for text generation)
- **PyPDF2** (PDF text extraction)

## Usage Guide
1. **Upload a PDF** via the sidebar.
2. **Select Prerequisite Knowledge** based on your familiarity.
3. **Generate a Study Plan** that structures learning into five detailed modules.
4. **Get Detailed Explanations** for each module.
5. **Generate & Answer Questions** to assess your understanding.

## Project Structure
```
📂 ai-pdf-study-assistant
├── app.py  # Streamlit UI
├── rag.py  # Retrieval-Augmented Generation logic
├── requirements.txt  # Dependencies
├── README.md  # Project Documentation
```

## Streamlit App
Access the application here: [StudySynth](https://studysynth.streamlit.app/)

## Future Enhancements
- Support for multi-PDF study plans.
- Enhanced personalization based on user preferences.
- Integration with note-taking apps.

## License
This project is open-source under the MIT License.


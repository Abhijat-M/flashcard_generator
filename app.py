import streamlit as st
from utils import extract_text, detect_topics
from flashcard_generator import generate_flashcards
import pandas as pd
import json

if "flashcards" not in st.session_state:
    st.session_state.flashcards = []

st.set_page_config(page_title="Flashcard Generator", layout="wide")
st.title("LLM-Powered Flashcard Generator")

st.sidebar.header("Input Options")
subject = st.sidebar.selectbox(
    "Select Subject Type",
    ["General", "Biology", "Computer Science", "History", "Math"]
)

# Upload file section
uploaded_file = st.file_uploader("Upload PDF or TXT file", type=["pdf", "txt"])
raw_text = ""

if uploaded_file:
    try:
        raw_text = extract_text(uploaded_file)
        st.success("File uploaded successfully!")
    except Exception as e:
        st.error(f"Error reading file: {e}")

# Text input area
manual_input = st.text_area("Or paste your text here", height=200)
final_text = manual_input or raw_text

if st.button("Generate Flashcards") and final_text:
    with st.spinner("Generating flashcards..."):
        result = generate_flashcards(final_text, subject)
        
        if "error" in result:
            st.error(result["error"])
        else:
            st.session_state.flashcards = result

# Display generated flashcards
if st.session_state.flashcards:
    st.subheader(f"Generated Flashcards ({len(st.session_state.flashcards)})")
    
    # Topic filter
    topic_names = ["All"] + list(set(c["topic"] for c in st.session_state.flashcards))
    selected_topic = st.selectbox("Filter by topic", topic_names)
    
    # Display cards
    for i, card in enumerate(st.session_state.flashcards):
        if selected_topic != "All" and card.get("topic", "General") != selected_topic:
            continue
            
        with st.expander(f"Card {i+1}: {card['question'][:50]}..."):
            st.markdown("**Question:** " + card["question"])
            st.markdown("**Answer:** " + card["answer"])
            st.markdown(f"*Topic: {card.get('topic', 'General')}*")

    # Export
    col1, col2, col3 = st.columns(3)
    
    with col1:
        df = pd.DataFrame(st.session_state.flashcards)
        st.download_button(
            "Download as CSV",
            data=df.to_csv(index=False),
            file_name="flashcards.csv",
            mime="text/csv"
        )
    
    with col2:
        st.download_button(
            "Download as JSON",
            data=json.dumps(st.session_state.flashcards, indent=2),
            file_name="flashcards.json",
            mime="application/json"
        )
    


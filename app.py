import streamlit as st

from chatbot import (
    build_qa_chain,
    save_chat_context
)

# ====================================
# PAGE CONFIG
# ====================================

st.set_page_config(
    page_title="University AI Assistant",
    page_icon="🎓",
    layout="centered"
)

# ====================================
# HEADER
# ====================================

st.title("🎓 University AI Assistant")

st.caption(
    "Ask questions about admissions, fees, hostel, exams, syllabus, and more."
)

# ====================================
# LOAD QA SYSTEM
# ====================================

def load_chain():

    return build_qa_chain()

# Initialize QA chain
if "qa_chain" not in st.session_state:

    with st.spinner(
        "Loading AI system..."
    ):

        st.session_state.qa_chain = (
            load_chain()
        )

# ====================================
# CHAT HISTORY
# ====================================

if "messages" not in st.session_state:

    st.session_state.messages = []

# Display old messages
for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):

        st.write(msg["content"])

# ====================================
# USER INPUT
# ====================================

question = st.chat_input(
    "Ask your question..."
)

if question:

    # Store user msg
    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    # Display user msg
    with st.chat_message("user"):

        st.write(question)

    # Generate answer
    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            answer = (
                st.session_state.qa_chain(
                    question
                )
            )

            st.write(answer)

    # Save chat
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )

    # Save memory
    save_chat_context(
        question,
        answer
    )
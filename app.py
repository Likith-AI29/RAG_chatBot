import streamlit as st
from chatbot import build_qa_chain, EMBEDDING_MODEL
from langchain_community.embeddings import HuggingFaceEmbeddings

@st.cache_resource
def load_embeddings():
    return HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

st.title("🎓 University Admission Chatbot")
st.caption("Ask me anything about admissions!")

if "qa_chain" not in st.session_state:
    with st.spinner("Loading knowledge base..."):
        embeddings = load_embeddings()
        st.session_state.qa_chain = build_qa_chain(embeddings)

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if question := st.chat_input("Ask a question..."):
    st.session_state.messages.append({"role": "user", "content": question})
    st.chat_message("user").write(question)

    answer = st.session_state.qa_chain.invoke(question)

    st.session_state.messages.append({"role": "assistant", "content": answer})
    st.chat_message("assistant").write(answer)

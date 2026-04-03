# 🎓 University Admission Chatbot

A simple RAG (Retrieval Augmented Generation) chatbot that answers university admission questions using a local knowledge base, HuggingFace embeddings, FAISS vector search, and a Hugging Face model as the LLM.

---

## How It Works

```
User Question
     ↓
Convert question to vector (HuggingFace - local)
     ↓
Search FAISS for relevant FAQ chunks
     ↓
Send matched context + question to the LLM
     ↓
LLM returns a natural language answer
     ↓
Streamlit displays it in chat UI
```

The chatbot only answers based on what is in `admission_faq.txt`. It does not hallucinate facts outside the document.

---

## Project Structure

```
my_chatBot/
├── admission_faq.txt   ← knowledge base (chatbot's brain)
├── chatbot.py          ← RAG chain logic
├── app.py              ← Streamlit chat UI
├── requirements.txt    ← Python dependencies
└── .gitignore          ← ignores environment files
```

---

## Tech Stack

| Tool | Purpose |
|---|---|
| Streamlit | Chat UI |
| LangChain | Glue between all components |
| HuggingFace `all-MiniLM-L6-v2` | Free local text embeddings |
| FAISS | In-memory vector search |
| HuggingFace `microsoft/phi-2` | LLM to generate answers |

---

## Prerequisites

- Python 3.9+

---

## Setup & Installation

**1. Clone or download the project**

```bash
cd my_chatBot
```

**2. Install dependencies**

```bash
pip install -r requirements.txt
```

**3. Run the chatbot**

```bash
streamlit run app.py
```

Open your browser at `http://localhost:8501`

---

## Example Questions to Ask

- What is the application deadline?
- What documents are required for admission?
- What is the tuition fee for postgraduate?
- How do I apply?

---

## Updating the Knowledge Base

To change what the chatbot knows, simply edit `admission_faq.txt` and restart the app. No retraining needed.

---

## Files Explained

### `chatbot.py`
- Loads `admission_faq.txt` using `TextLoader`
- Converts text into vectors using `HuggingFaceEmbeddings` (runs locally)
- Stores vectors in a `FAISS` in-memory database
- Builds an LCEL chain: `retriever → prompt → LLM → string output`

### `app.py`
- Streamlit UI with chat history using `st.session_state`
- Loads the RAG chain once on startup using `st.session_state` to avoid re-embedding on every message
- Uses `st.chat_input` and `st.chat_message` for a proper chat interface

### `admission_faq.txt`
- Plain text knowledge base
- Contains all facts the chatbot can answer
- Can be replaced with any topic

---

## Dependencies

```
langchain
langchain-core
langchain-community
langchain-huggingface
faiss-cpu
streamlit
pypdf
sentence-transformers
```

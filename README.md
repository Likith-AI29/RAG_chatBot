# 🎓 University Admission Chatbot (RAG + Category Routing)

A local **Retrieval-Augmented Generation (RAG)** chatbot that answers university questions using:
- your documents under `documents/`
- **HuggingFace embeddings** (local)
- **FAISS** for similarity search
- an **Ollama**-hosted LLM (default: `gemma4:e2b`)

The app classifies each question into a category (finance/academics/hostel/etc.), retrieves the most relevant chunks, then formats an answer using a category-specific prompt.

---

## How it works

1. **User asks a question** in the Streamlit UI (`app.py`).
2. `chatbot.py` **loads/creates the FAISS index** from `documents/`.
3. The question is **classified** using keyword routing (`router/classifier.py`).
4. The retriever fetches top chunks:
   - If category is `general` → no filter
   - Otherwise → filter by `doc.metadata["category"]`
5. A **prompt template** is selected by category (`router/router.py`).
6. The LLM (Ollama) generates the final answer.

---

## Features

- Supports documents in `documents/<category>/` with both **`.txt`** and **`.pdf`**
- Uses metadata filtering so finance questions search only finance docs (and so on)
- Uses chat history inside prompts (`memory.save_context()`)
- Uses a local embedding model: `sentence-transformers/all-MiniLM-L6-v2`

---

## Repo structure

```
RAG_chatBot/
├── app.py                      # Streamlit UI
├── chatbot.py                  # RAG chain logic
├── documents/                 
│   ├── admissions/            # *.txt / *.pdf
│   ├── academics/
│   ├── finance/
│   ├── hostel/
│   └── placements/
├── faiss_index/              
│   ├── index.faiss            # existing FAISS index (auto-loaded)
│   └── index.pkl             
├── router/
│   ├── classifier.py         # keyword category classifier
│   └── router.py             # prompt selection
├── prompts/
│   ├── general_prompt.py
│   ├── finance_prompt.py
│   ├── academic_prompt.py
│   └── hostel_prompt.py
├── retrieval/                
│   ├── vectorstore.py         # vectorstore utilities (if used)
│   └── hybrid_search.py      # hybrid retrieval utilities (if used)
└── memory/
    └── conversation_memory.py # (or Simple memory inside chatbot.py)
```

---

## Tech stack

- **Streamlit**: chat UI
- **LangChain**: loaders, prompts, retrieval glue
- **LangChain Community FAISS**: vector store
- **HuggingFaceEmbeddings**: `sentence-transformers/all-MiniLM-L6-v2`
- **OllamaLLM**: `gemma4:e2b` (configured in `chatbot.py`)
- **TextSplitter**: `RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)`

---

## Prerequisites

- Python 3.9+
- **Ollama installed** and running
- The model `gemma4:e2b` available in Ollama

---

## Setup & Installation

1) Install dependencies

```bash
pip install -r requirements.txt
```

2) Start the app

```bash
streamlit run app.py
```

3) Open the app in your browser (default):

`http://localhost:8501`

---

## Question categories & prompt routing

`router/classifier.py` uses keyword matching to assign a category:
- `finance`
- `academics`
- `hostel`
- `admissions`
- `placements`
- `general` (fallback)

`router/router.py` maps categories to prompt templates for:
- `finance` → `FINANCE_PROMPT`
- `academics` → `ACADEMIC_PROMPT`
- `hostel` → `HOSTEL_PROMPT`
- `general` → `GENERAL_PROMPT`

If the classifier returns a category without a dedicated prompt (e.g., `admissions`, `placements`), the system falls back to the **general prompt**.

---

## Knowledge base (documents) & updates

### Where knowledge comes from
The bot reads **everything under**:
- `documents/admissions/`
- `documents/academics/`
- `documents/finance/`
- `documents/hostel/`
- `documents/placements/`

Supported file types per folder:
- `.txt`
- `.pdf`

Each chunk gets metadata:
- `category` = folder name
- `source_file` = filename

### Rebuilding the FAISS index
`chatbot.py` checks for `faiss_index/index.faiss`:
- If it exists → it is loaded
- If it does not exist → embeddings are created and a new FAISS index is saved

If you change documents and want the index rebuilt, delete `faiss_index/` (or at least `index.faiss`) and restart the app.

---

## Example questions

- Finance: “What is the tuition fee?”
- Academics: “When are the exams for semester 2?”
- Hostel: “What are the hostel room rules?”
- Admissions: “How do I apply for admission?”
- Placements: “Which companies come for recruitment?”

---

## Notes

- The system is intended to answer from retrieved context. If context doesn’t include the info, prompts instruct the model to say **"I don't know"**.


import os

from dotenv import load_dotenv

# ====================================
# ROUTER
# ====================================

from router.router import get_prompt
from router.classifier import classify_query

# ====================================
# DOCUMENT LOADERS
# ====================================

from langchain_community.document_loaders import (
    TextLoader,
    PyPDFLoader
)

# ====================================
# VECTOR STORE
# ====================================

from langchain_community.vectorstores import FAISS

from langchain_community.embeddings import (
    HuggingFaceEmbeddings
)

# ====================================
# LLM
# ====================================

from langchain_ollama import OllamaLLM

# ====================================
# TEXT SPLITTER
# ====================================

from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)

load_dotenv()

# ====================================
# CONFIG
# ====================================

EMBEDDING_MODEL = (
    "sentence-transformers/all-MiniLM-L6-v2"
)

DOCUMENTS_PATH = "documents"

DB_PATH = "faiss_index"

TOP_K = 3

# ====================================
# SIMPLE MEMORY
# ====================================

class SimpleConversationBufferMemory:

    def __init__(self):

        self.buffer = []

    def load_memory(self):

        if not self.buffer:

            return ""

        return "\n".join(self.buffer)

    def save_context(
        self,
        question,
        answer
    ):

        self.buffer.append(
            f"User: {question}"
        )

        self.buffer.append(
            f"Assistant: {answer}"
        )

# ====================================
# MEMORY INSTANCE
# ====================================

memory = SimpleConversationBufferMemory()

# ====================================
# FORMAT DOCS
# ====================================

def format_docs(docs):

    return "\n\n".join(
        doc.page_content
        for doc in docs
    )

# ====================================
# LOAD DOCUMENTS
# ====================================

def load_documents():

    all_documents = []

    # Category folders
    for category in os.listdir(
        DOCUMENTS_PATH
    ):

        category_path = os.path.join(
            DOCUMENTS_PATH,
            category
        )

        if not os.path.isdir(
            category_path
        ):

            continue

        # Files inside category
        for file in os.listdir(
            category_path
        ):

            file_path = os.path.join(
                category_path,
                file
            )

            docs = []

            # TXT
            if file.endswith(".txt"):

                loader = TextLoader(
                    file_path
                )

                docs = loader.load()

            # PDF
            elif file.endswith(".pdf"):

                loader = PyPDFLoader(
                    file_path
                )

                docs = loader.load()

            else:

                continue

            # Metadata
            for doc in docs:

                doc.metadata[
                    "category"
                ] = category

                doc.metadata[
                    "source_file"
                ] = file

            all_documents.extend(docs)

    return all_documents

# ====================================
# VECTOR DATABASE
# ====================================

def get_vectorstore():

    embeddings = (
        HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL
        )
    )

    faiss_file = os.path.join(
        DB_PATH,
        "index.faiss"
    )

    # LOAD EXISTING DB
    if os.path.exists(faiss_file):

        print(
            "Loading existing FAISS index..."
        )

        db = FAISS.load_local(
            DB_PATH,
            embeddings,
            allow_dangerous_deserialization=True
        )

    # CREATE NEW DB
    else:

        print(
            "Creating new FAISS index..."
        )

        documents = load_documents()

        print(
            f"Loaded {len(documents)} documents"
        )

        splitter = (
            RecursiveCharacterTextSplitter(
                chunk_size=500,
                chunk_overlap=50
            )
        )

        split_docs = (
            splitter.split_documents(
                documents
            )
        )

        print(
            f"Created {len(split_docs)} chunks"
        )

        db = FAISS.from_documents(
            split_docs,
            embeddings
        )

        db.save_local(DB_PATH)

        print(
            "FAISS index saved locally."
        )

    return db

# ====================================
# BUILD QA SYSTEM
# ====================================

def build_qa_chain():

    # ====================================
    # VECTOR DB
    # ====================================

    db = get_vectorstore()

    # ====================================
    # LLM
    # ====================================

    llm = OllamaLLM(
        model="gemma4:e2b",
        temperature=0.2
    )

    # ====================================
    # RESPONSE FUNCTION
    # ====================================

    def generate_response(question):

        # ----------------------------
        # CLASSIFY QUERY
        # ----------------------------

        classification = classify_query(
            question
        )

        category = classification[
            "category"
        ]

        confidence = classification[
            "confidence"
        ]

        print("\n================")
        print(f"Question: {question}")
        print(f"Category: {category}")
        print(f"Confidence: {confidence}")
        print("================\n")

        # ----------------------------
        # RETRIEVER
        # ----------------------------

        if category == "general":

            retriever = db.as_retriever(
                search_kwargs={
                    "k": TOP_K
                }
            )

        else:

            retriever = db.as_retriever(
                search_kwargs={
                    "k": TOP_K,
                    "filter": {
                        "category": category
                    }
                }
            )

        docs = retriever.invoke(
            question
        )

        # DEBUG
        print("\nRetrieved Docs:")

        for doc in docs:

            print(doc.metadata)

        # ----------------------------
        # FORMAT CONTEXT
        # ----------------------------

        context = format_docs(docs)

        # ----------------------------
        # PROMPT
        # ----------------------------

        prompt_template = get_prompt(
            category
        )

        # ----------------------------
        # MEMORY
        # ----------------------------

        chat_history = (
            memory.load_memory()
        )

        # ----------------------------
        # FINAL PROMPT
        # ----------------------------

        final_prompt = (
            prompt_template.format(
                context=context,
                question=question,
                chat_history=chat_history
            )
        )

        # DEBUG
        print("\nPROMPT:")
        print(final_prompt[:2000])

        # ----------------------------
        # GENERATE RESPONSE
        # ----------------------------

        response = llm.invoke(
            final_prompt
        )

        return response

    # IMPORTANT
    return generate_response

# ====================================
# SAVE MEMORY
# ====================================

def save_chat_context(
    question,
    answer
):

    memory.save_context(
        question,
        answer
    )
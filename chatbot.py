import os
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

load_dotenv()

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

PROMPT = ChatPromptTemplate.from_template(
    "Answer the question using ONLY the context below.\n"
    "If the answer is not in the context, say 'I don't know'.\n\n"
    "Context:\n{context}\n\n"
    "Question: {question}\n\n"
    "Answer:"
)

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def build_qa_chain(embeddings, faq_path: str = "admission_faq.txt"):
    documents = TextLoader(faq_path).load()
    db = FAISS.from_documents(documents, embeddings)

    # Local Ollama Phi3 model
    llm = OllamaLLM(
        model="phi3",
        temperature=0
    )

    return (
        {"context": db.as_retriever() | format_docs, "question": RunnablePassthrough()}
        | PROMPT
        | llm
        | StrOutputParser()
    )

if __name__ == "__main__":
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    chain = build_qa_chain(embeddings)
    print(chain.invoke("What documents are required for admission?"))
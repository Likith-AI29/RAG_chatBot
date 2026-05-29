from langchain_core.prompts import ChatPromptTemplate

GENERAL_PROMPT = ChatPromptTemplate.from_template(
    """
You are a helpful university assistant.

Answer ONLY using the provided context.

If the answer is not found,
say "I don't know".

Chat History:
{chat_history}

Context:
{context}

Question:
{question}

Answer:
"""
)
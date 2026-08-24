import requests

from .embeddings import create_embeddings
from .vector_store import similarity_search


# ============================================================
# Ollama Settings
# ============================================================

OLLAMA_URL = "http://localhost:11434/api/generate"

MODEL_NAME = "llama3.2"


# ============================================================
# Ask Question
# ============================================================

def ask_question(question: str):

    # --------------------------------------------------------
    # Create embedding for question
    # --------------------------------------------------------

    query_embedding = create_embeddings(
        [question]
    )


    # --------------------------------------------------------
    # Search vector database
    # --------------------------------------------------------

    results = similarity_search(
        query_embedding[0],
        top_k=3
    )


    # --------------------------------------------------------
    # No relevant information
    # --------------------------------------------------------

    if not results:

        return {

            "answer":
                "The information was not found in the uploaded document.",

            "sources": []

        }


    # --------------------------------------------------------
    # Extract text from retrieved chunks
    # --------------------------------------------------------

    context_parts = []

    clean_sources = []


    for result in results:

        # If result is a string

        if isinstance(result, str):

            text = result


        # If result is a dictionary

        elif isinstance(result, dict):

            text = (
                result.get("text")
                or result.get("content")
                or result.get("chunk")
                or result.get("page_content")
                or ""
            )


        else:

            text = str(result)


        if text.strip():

            context_parts.append(text)

            clean_sources.append({

                "text": text

            })


    # --------------------------------------------------------
    # Create context
    # --------------------------------------------------------

    context = "\n\n".join(
        context_parts
    )


    # --------------------------------------------------------
    # Prompt
    # --------------------------------------------------------

    prompt = f"""
You are a document question-answering assistant.

Answer the user's question ONLY using the information
provided in the document context below.

If the answer cannot be found in the document,
say exactly:

"The information was not found in the uploaded document."

Do not use outside knowledge.

DOCUMENT CONTEXT:
-----------------
{context}
-----------------

USER QUESTION:
{question}

ANSWER:
"""


    # --------------------------------------------------------
    # Send request to Ollama
    # --------------------------------------------------------

    response = requests.post(

        OLLAMA_URL,

        json={

            "model": MODEL_NAME,

            "prompt": prompt,

            "stream": False

        },

        timeout=120

    )


    # --------------------------------------------------------
    # Check response
    # --------------------------------------------------------

    response.raise_for_status()


    data = response.json()


    answer = data.get(
        "response",
        "The information was not found in the uploaded document."
    )


    # --------------------------------------------------------
    # Return clean result
    # --------------------------------------------------------

    return {

        "answer": answer.strip(),

        "sources": clean_sources

    }
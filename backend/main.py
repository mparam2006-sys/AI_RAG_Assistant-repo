import os
import shutil

from fastapi import FastAPI, UploadFile, File

from fastapi.middleware.cors import CORSMiddleware

from fastapi.staticfiles import StaticFiles


from .document_processor import (
    extract_text,
    split_text
)

from .embeddings import (
    create_embeddings
)

from .vector_store import (
    create_vector_store
)

from .rag import (
    ask_question
)


# ============================================================
# FastAPI
# ============================================================

app = FastAPI(

    title="AI RAG Document Assistant",

    description=
        "Retrieval-Augmented Generation Document Assistant",

    version="1.0"

)


# ============================================================
# CORS
# ============================================================

app.add_middleware(

    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]

)


# ============================================================
# Folders
# ============================================================

UPLOAD_FOLDER = "uploads"

VECTORSTORE_FOLDER = "vectorstore"


os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)

os.makedirs(
    VECTORSTORE_FOLDER,
    exist_ok=True
)


# ============================================================
# Frontend
# ============================================================

app.mount(

    "/frontend",

    StaticFiles(
        directory="frontend",
        html=True
    ),

    name="frontend"

)


# ============================================================
# Home
# ============================================================

@app.get("/")
def home():

    return {

        "message":
            "AI RAG Document Assistant is running!",

        "frontend":
            "/frontend",

        "documentation":
            "/docs"

    }


# ============================================================
# Upload Document
# ============================================================

@app.post("/upload")
async def upload_document(

    file: UploadFile = File(...)

):

    allowed_extensions = {

        ".pdf",
        ".txt"

    }


    extension = os.path.splitext(

        file.filename

    )[1].lower()


    if extension not in allowed_extensions:

        return {

            "success": False,

            "message":
                "Only PDF and TXT files are allowed."

        }


    # --------------------------------------------------------
    # Save File
    # --------------------------------------------------------

    file_path = os.path.join(

        UPLOAD_FOLDER,

        file.filename

    )


    try:

        with open(

            file_path,

            "wb"

        ) as buffer:

            shutil.copyfileobj(

                file.file,

                buffer

            )


        # ----------------------------------------------------
        # Extract
        # ----------------------------------------------------

        text = extract_text(

            file_path

        )


        if not text.strip():

            return {

                "success": False,

                "message":
                    "No readable text was found."

            }


        # ----------------------------------------------------
        # Chunk
        # ----------------------------------------------------

        chunks = split_text(

            text

        )


        if not chunks:

            return {

                "success": False,

                "message":
                    "Could not create document chunks."

            }


        # ----------------------------------------------------
        # Embeddings
        # ----------------------------------------------------

        embeddings = create_embeddings(

            chunks

        )


        # ----------------------------------------------------
        # FAISS
        # ----------------------------------------------------

        number_of_chunks = create_vector_store(

            chunks,

            embeddings

        )


        return {

            "success": True,

            "filename":
                file.filename,

            "chunks":
                number_of_chunks,

            "message":
                "Document uploaded and processed successfully."

        }


    except Exception as error:

        return {

            "success": False,

            "message":
                f"Error processing document: {str(error)}"

        }


# ============================================================
# Ask Question
# ============================================================

@app.post("/ask")
async def ask_question_endpoint(

    data: dict

):

    question = data.get(

        "question",

        ""

    ).strip()


    if not question:

        return {

            "success": False,

            "answer":
                "Please enter a question.",

            "sources": []

        }


    try:

        result = ask_question(

            question

        )


        return {

            "success": True,

            "answer":
                result.get(
                    "answer",
                    ""
                ),

            "sources":
                result.get(
                    "sources",
                    []
                )

        }


    except Exception as error:

        return {

            "success": False,

            "answer":
                f"Error: {str(error)}",

            "sources": []

        }
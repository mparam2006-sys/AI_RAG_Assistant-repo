# AI RAG Document Assistant

An AI-powered **Retrieval-Augmented Generation (RAG) Document
Assistant** that allows users to upload PDF or TXT documents and ask
questions about their contents.

The system extracts text from the uploaded document, splits it into
smaller chunks, creates embeddings, stores them in a FAISS vector store,
retrieves the most relevant chunks for a question, and generates a
context-based answer.

------------------------------------------------------------------------

## ✨ Features

-   📄 Upload PDF and TXT documents
-   🔍 Extract text from documents
-   ✂️ Split documents into smaller chunks
-   🧠 Generate text embeddings
-   🗂️ Store embeddings using FAISS
-   🔎 Perform similarity search
-   💬 Ask questions about the uploaded document
-   🤖 Generate answers using the RAG pipeline
-   📚 Display retrieved document context
-   🌐 FastAPI backend with HTML/CSS/JavaScript frontend
-   📱 Responsive frontend design

------------------------------------------------------------------------

## Project Structure

``` text
AI_RAG_Document_Assistant/
│
├── backend/
│   ├── main.py
│   ├── document_processor.py
│   ├── embeddings.py
│   ├── vector_store.py
│   └── rag.py
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── uploads/
│
├── vectorstore/
│
├── venv/
│
└── README.md
```

------------------------------------------------------------------------

## RAG Workflow

``` text
PDF / TXT Upload
       ↓
Text Extraction
       ↓
Text Chunking
       ↓
Embeddings Generation
       ↓
FAISS Vector Store
       ↓
User Question
       ↓
Similarity Search
       ↓
Relevant Context
       ↓
LLM / RAG
       ↓
Context-Based Answer
```

------------------------------------------------------------------------

## Technologies Used

### Backend

-   Python
-   FastAPI
-   Uvicorn
-   Python Multipart

### Document Processing

-   PyMuPDF

### Embeddings

-   Sentence Transformers

### Vector Database

-   FAISS

### Text Splitting

-   LangChain Text Splitters

### Frontend

-   HTML
-   CSS
-   JavaScript

------------------------------------------------------------------------

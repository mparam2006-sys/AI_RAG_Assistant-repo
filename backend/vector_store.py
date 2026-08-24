import os
import pickle

import faiss
import numpy as np


# ============================================================
# Storage
# ============================================================

VECTORSTORE_FOLDER = "vectorstore"

INDEX_FILE = os.path.join(
    VECTORSTORE_FOLDER,
    "index.faiss"
)

CHUNKS_FILE = os.path.join(
    VECTORSTORE_FOLDER,
    "chunks.pkl"
)


os.makedirs(
    VECTORSTORE_FOLDER,
    exist_ok=True
)


# ============================================================
# Create Vector Store
# ============================================================

def create_vector_store(
    chunks,
    embeddings
):

    # Convert embeddings to numpy

    vectors = np.array(
        embeddings,
        dtype="float32"
    )


    # Create FAISS index

    dimension = vectors.shape[1]

    index = faiss.IndexFlatL2(
        dimension
    )


    # Add vectors

    index.add(vectors)


    # Save FAISS index

    faiss.write_index(
        index,
        INDEX_FILE
    )


    # Save chunks

    with open(
        CHUNKS_FILE,
        "wb"
    ) as file:

        pickle.dump(
            chunks,
            file
        )


    return len(chunks)


# ============================================================
# Similarity Search
# ============================================================

def similarity_search(
    query_embedding,
    top_k=3
):

    # Check if database exists

    if not os.path.exists(
        INDEX_FILE
    ):

        return []


    if not os.path.exists(
        CHUNKS_FILE
    ):

        return []


    # Load FAISS index

    index = faiss.read_index(
        INDEX_FILE
    )


    # Load chunks

    with open(
        CHUNKS_FILE,
        "rb"
    ) as file:

        chunks = pickle.load(
            file
        )


    # Convert query embedding

    query_vector = np.array(

        [query_embedding],

        dtype="float32"

    )


    # Search

    distances, indices = index.search(

        query_vector,

        min(
            top_k,
            len(chunks)
        )

    )


    # Retrieve chunks

    results = []


    for index_number in indices[0]:

        if index_number == -1:

            continue


        results.append(
            chunks[index_number]
        )


    return results
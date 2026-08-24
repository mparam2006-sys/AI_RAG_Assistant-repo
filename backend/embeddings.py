from sentence_transformers import SentenceTransformer


# ============================================================
# Embedding Model
# ============================================================

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


# ============================================================
# Create Embeddings
# ============================================================

def create_embeddings(texts):

    embeddings = model.encode(

        texts,

        convert_to_numpy=True

    )


    return embeddings
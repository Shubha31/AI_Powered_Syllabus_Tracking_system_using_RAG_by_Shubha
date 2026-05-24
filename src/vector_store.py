from pathlib import Path
from uuid import uuid4

import chromadb

from src.config import CHROMA_PATH, COLLECTION_NAME


def get_collection():
    Path(CHROMA_PATH).mkdir(parents=True, exist_ok=True)
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    return client.get_or_create_collection(name=COLLECTION_NAME)


def add_chunks(chunks, embeddings, metadata):
    collection = get_collection()

    ids = [str(uuid4()) for _ in chunks]
    metadatas = []
    for index, _ in enumerate(chunks):
        item = dict(metadata)
        item["chunk_index"] = index
        metadatas.append(item)

    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings,
        metadatas=metadatas,
    )


def search_chunks(query_embedding, top_k=5):
    collection = get_collection()
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
    )

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0]

    matches = []
    for document, metadata, distance in zip(documents, metadatas, distances):
        matches.append(
            {
                "text": document,
                "metadata": metadata,
                "score": 1 / (1 + distance),
            }
        )
    return matches

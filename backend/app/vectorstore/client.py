import chromadb

def get_vectorstore():
    client = chromadb.PersistentClient(
        path="./chroma_db"
    )

    return client

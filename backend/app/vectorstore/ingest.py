import os
import time
from pypdf import PdfReader
import cohere
from dotenv import load_dotenv
from cohere.errors import TooManyRequestsError

from app.vectorstore.client import get_vectorstore
from app.rag.chunking import chunk_text
from app.metadata.infer import infer_metadata

load_dotenv()

COHERE_API_KEY = os.getenv("COHERE_API_KEY")
co = cohere.ClientV2(api_key=COHERE_API_KEY)

PDF_BASE_PATH = "data/pdfs"

# Límite de batch para embeddings
# batch es una lista de textos a embedder
BATCH_SIZE = 10


def ingest_pdfs():
    client = get_vectorstore()
    collection = client.get_or_create_collection(name="documentation")

    for doc_type in ["tecnicos", "sistemas"]:
        folder_path = os.path.join(PDF_BASE_PATH, doc_type)

        if not os.path.isdir(folder_path):
            continue

        for filename in os.listdir(folder_path):
            if not filename.endswith(".pdf"):
                continue

            file_path = os.path.join(folder_path, filename)
            reader = PdfReader(file_path)

            # 🔎 Inferimos metadata UNA sola vez por documento
            base_metadata = infer_metadata(doc_type, filename)

            # 🔧 Corrección robusta de subtipo (fiscal / no_fiscal)
            filename_lower = filename.lower()
            if "no_fiscal" in filename_lower:
                base_metadata["subtipo"] = "no_fiscal"
            elif "fiscal" in filename_lower:
                base_metadata["subtipo"] = "fiscal"

            print(f"📄 Procesando {doc_type}/{filename}")
            print(f"   ↳ metadata: {base_metadata}")

            # 👉 AHORA recorremos TODAS las páginas
            for page_number, page in enumerate(reader.pages, start=1):
                text = page.extract_text()
                if not text:
                    continue

                chunks = chunk_text(text)

                for start in range(0, len(chunks), BATCH_SIZE):
                    batch_chunks = chunks[start:start + BATCH_SIZE]

                    try:
                        response = co.embed(
                            model="embed-multilingual-v3.0",
                            texts=batch_chunks,
                            input_type="search_document"
                        )

                        embeddings = response.embeddings.float

                        for i, (chunk, embedding) in enumerate(zip(batch_chunks, embeddings)):
                            metadata = {
                                **base_metadata,
                                "page": page_number
                            }

                            collection.add(
                                documents=[chunk],
                                embeddings=[embedding],
                                metadatas=[metadata],
                                ids=[f"{doc_type}_{filename}_{page_number}_{start + i}"]
                            )

                        # pausa para evitar rate limit
                        time.sleep(1)

                    except TooManyRequestsError:
                        print("⏸️ Rate limit alcanzado. Esperando 60 segundos...")
                        time.sleep(60)

    print("✅ Ingesta completada correctamente")


if __name__ == "__main__":
    ingest_pdfs()

# ejecutar con:
# python -m app.vectorstore.ingest

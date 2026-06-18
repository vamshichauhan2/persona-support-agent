import os

from dotenv import load_dotenv
import chromadb

from sentence_transformers import SentenceTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pypdf import PdfReader

load_dotenv()

class LocalRAGPipeline:

    def __init__(self):

        self.embedding_model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

        self.chroma_client = chromadb.PersistentClient(
            path="./chroma_db"
        )

        try:
            self.chroma_client.delete_collection(
                "support_kb"
            )
        except:
            pass

        self.collection = self.chroma_client.get_or_create_collection(
            name="support_kb"
        )

    def get_embedding(self, text):

        return self.embedding_model.encode(
            text
        ).tolist()

    def load_documents(self):

        documents = []

        data_folder = "data"

        for filename in os.listdir(data_folder):

            path = os.path.join(
                data_folder,
                filename
            )

            if filename.endswith(".md"):

                with open(
                    path,
                    "r",
                    encoding="utf-8"
                ) as file:

                    documents.append(
                        {
                            "source": filename,
                            "content": file.read()
                        }
                    )

            elif filename.endswith(".txt"):

                with open(
                    path,
                    "r",
                    encoding="utf-8"
                ) as file:

                    documents.append(
                        {
                            "source": filename,
                            "content": file.read()
                        }
                    )

            elif filename.endswith(".pdf"):

                try:

                    reader = PdfReader(path)

                    pdf_text = ""

                    for page in reader.pages:

                        extracted = page.extract_text()

                        if extracted:
                            pdf_text += extracted + "\n"

                    documents.append(
                        {
                            "source": filename,
                            "content": pdf_text
                        }
                    )

                except Exception as e:

                    print(
                        f"Skipping PDF {filename}: {e}"
                    )

        return documents

    def ingest_documents(self):

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50
        )

        documents = self.load_documents()

        total_chunks = 0

        for doc in documents:

            chunks = splitter.split_text(
                doc["content"]
            )

            for index, chunk in enumerate(chunks):

                embedding = self.get_embedding(
                    chunk
                )

                chunk_id = (
                    f"{doc['source']}_{index}"
                )

                self.collection.add(
                    ids=[chunk_id],
                    embeddings=[embedding],
                    documents=[chunk],
                    metadatas=[
                        {
                            "source": doc["source"],
                            "chunk_index": index
                        }
                    ]
                )

                total_chunks += 1

        print(
            f"Knowledge Base Indexed Successfully ({total_chunks} chunks)"
        )

    def retrieve_context(
        self,
        query,
        top_k=3
    ):

        query_embedding = self.get_embedding(
            query
        )

        results = self.collection.query(
            query_embeddings=[
                query_embedding
            ],
            n_results=top_k
        )

        retrieved = []

        if results["documents"]:

            for i in range(
                len(results["documents"][0])
            ):

                distance = 0

                if (
                    "distances" in results
                    and results["distances"]
                ):
                    distance = round(
                        results["distances"][0][i],
                        4
                    )

                score = round(
                    1 - distance,
                    4
                )

                retrieved.append(
                    {
                        "text":
                        results["documents"][0][i],

                        "source":
                        results["metadatas"][0][i]["source"],

                        "score":
                        score
                    }
                )

        return retrieved

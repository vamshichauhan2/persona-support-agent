from src.rag_pipeline import LocalRAGPipeline

rag = LocalRAGPipeline()

rag.ingest_documents()

query = "How do I reset my password?"

results = rag.retrieve_context(query)

for item in results:

    print("\nSOURCE:", item["source"])

    print("\nSCORE:", item["score"])

    print("\nTEXT:")
    print(item["text"])
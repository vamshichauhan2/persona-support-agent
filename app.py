from src.classifier import classify_persona
from src.rag_pipeline import LocalRAGPipeline

rag = LocalRAGPipeline()

rag.ingest_documents()

query = input(
"Enter your message: "
)

persona = classify_persona(
query
)

print("\n==============================")
print("Detected Persona")
print("==============================")

print(
f"Persona: {persona['persona']}"
)

print(
f"Confidence: {persona['confidence']}"
)

print(
f"Reason: {persona['reasoning']}"
)

results = rag.retrieve_context(
query
)

print("\n==============================")
print("Retrieved Sources")
print("==============================")

for item in results:

    print(
        f"\nSource: {item['source']}"
    )

    print(
        f"Score: {item['score']}"
    )

    print(
        f"Content Preview: {item['text'][:150]}"
    )


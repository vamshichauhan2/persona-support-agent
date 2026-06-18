from src.classifier import classify_persona
from src.rag_pipeline import LocalRAGPipeline

from src.generator import generate_response

from src.escalator import (
    should_escalate,
    generate_handoff
)

rag = LocalRAGPipeline()

rag.ingest_documents()

query = input(
    "Enter your message: "
)

persona = classify_persona(
    query
)

results = rag.retrieve_context(
    query
)

escalate, reason = (
    should_escalate(
        query,
        results
    )
)

print("\n===================")
print("PERSONA")
print("===================")

print(persona)

print("\n===================")
print("RETRIEVAL")
print("===================")

for item in results:

    print(
        item["source"],
        item["score"]
    )

if escalate:

    print("\n===================")
    print("ESCALATED")
    print("===================")

    print(reason)

    print(
        generate_handoff(
            persona,
            query,
            results
        )
    )

else:

    response = generate_response(
        query,
        persona,
        results
    )

    print("\n===================")
    print("RESPONSE")
    print("===================")

    print(response)
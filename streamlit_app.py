import streamlit as st

from src.classifier import classify_persona
from src.rag_pipeline import LocalRAGPipeline
from src.generator import generate_response
from src.escalator import should_escalate, generate_handoff

st.title("Persona Adaptive Customer Support Agent")

@st.cache_resource
def load_rag():
    rag = LocalRAGPipeline()
    rag.ingest_documents()
    return rag

rag = load_rag()

query = st.text_input(
    "Ask a support question"
)

if query:

    persona = classify_persona(query)

    results = rag.retrieve_context(query)

    st.subheader("Detected Persona")

    st.json(persona)

    st.subheader("Retrieved Sources")

    for item in results:

        st.write(
            f"{item['source']} | Score: {item['score']}"
        )

    escalate, reason = should_escalate(
        query,
        results
    )

    if escalate:

        st.error(
            f"Escalated: {reason}"
        )

        st.json(
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

        st.success(response)
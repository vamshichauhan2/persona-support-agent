import json

SENSITIVE_KEYWORDS = [
    "billing",
    "refund",
    "legal",
    "lawsuit",
    "chargeback",
    "account deletion",
    "duplicate charge"
]


def should_escalate(user_query, retrieved_chunks):

    text = user_query.lower()

    for keyword in SENSITIVE_KEYWORDS:
        if keyword in text:
            return (
                True,
                f"Sensitive topic detected: {keyword}"
            )

    if not retrieved_chunks:
        return (
            True,
            "No relevant documents found"
        )

    best_score = max(
        [
            chunk["score"]
            for chunk in retrieved_chunks
        ]
    )

    if best_score < 0.30:
        return (
            True,
            f"Low retrieval confidence ({best_score})"
        )

    return (
        False,
        None
    )


def generate_handoff(
    persona,
    query,
    retrieved_chunks
):

    handoff = {
        "persona":
        persona["persona"],

        "issue":
        query,

        "documents_used":
        [
            chunk["source"]
            for chunk in retrieved_chunks
        ],

        "attempted_steps":
        [
            "Knowledge Base Search"
        ],

        "recommendation":
        "Human review required"
    }

    return json.dumps(
        handoff,
        indent=4
    )
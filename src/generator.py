import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv(
        "GEMINI_API_KEY"
    )
)


def generate_response(
    query,
    persona,
    retrieved_chunks
):

    context = "\n\n".join(
        [
            chunk["text"]
            for chunk in retrieved_chunks
        ]
    )

    persona_type = persona["persona"]

    if persona_type == "Technical Expert":

        style = """
Provide:
- Detailed explanation
- Root cause analysis
- Technical troubleshooting
- Step-by-step guidance
"""

    elif persona_type == "Frustrated User":

        style = """
Provide:
- Empathy
- Simple language
- Reassurance
- Actionable steps
"""

    else:

        style = """
Provide:
- Concise response
- Business impact
- Resolution guidance
- Timeline focus
"""

    prompt = f"""
You are a customer support agent.

Use ONLY the provided context.

{style}

Context:

{context}

User Question:

{query}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text
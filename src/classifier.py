import os
import json

from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def classify_persona(user_message: str):

    prompt = f"""
You are a customer persona classification engine.

Classify the user into EXACTLY ONE category:

1. Technical Expert
- Uses technical terminology
- Requests logs
- APIs
- Configuration
- Debugging details

2. Frustrated User
- Emotional language
- Complaints
- Urgency
- Anger
- Repeated issues

3. Business Executive
- Business impact
- Revenue
- Timeline
- Operations
- Outcome focused

Return ONLY valid JSON in this format:

{{
    "persona": "Technical Expert",
    "confidence": 0.95,
    "reasoning": "Reason for classification"
}}

User Message:
{user_message}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    text = response.text.strip()

    if text.startswith("```json"):
        text = text.replace("```json", "").replace("```", "").strip()

    return json.loads(text)


if __name__ == "__main__":

    test_message = (
        "How does this issue impact operations and when will it be resolved?"
    )

    result = classify_persona(test_message)

    print(json.dumps(result, indent=4))